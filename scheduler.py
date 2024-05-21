import logging
import traceback
import schedule
import time
import dataframe_image as dfi
from datetime import datetime
from configparser import ConfigParser
from nh_click_class import 반복작업, 기본환경설정
from telebot import TeleBot
import nest_asyncio

nest_asyncio.apply()

formater = logging.Formatter("%(asctime)s - [%(filename)s:%(lineno)d] %(levelname)s -> %(message)s")

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - [%(filename)s:%(lineno)d] %(levelname)s -> %(message)s')
logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
#
# logger.addHandler(logging.StreamHandler())
# fileHandler = logging.FileHandler("test.log")
# fileHandler.setLevel(logging.INFO)
# fileHandler.setFormatter(formater)
# logger.addHandler(fileHandler)

config = ConfigParser()
config.read("config.ini")

# config=pd.read_excel('config.xlsx')
# '이미지경로'
image_path = config["images"]["dir"]

# 대출상환단계
step=config["loan"]["step"]


main_job_done = False

log_print = None  # 로그를 찍기위한 함수

bot = TeleBot()
start_t = None
end_t = None

def start_scheduler(start_time, end_time, logfunc):
    global start_t
    global end_t

    start_t = start_time
    end_t = end_time
    """
    스케줄러 이용해서 프로그램 돌리기
    :param start_time: 프로그램 시작시간
    :param end_time: 프로그램 끝내는 시간
    :param logfunc: 로그 찍어주기
    :return: main1, repetition_work작업을 자동으로  정해진 시간에 진행하고 마치기.
    """
    global log_print
    log_print = logfunc
    logger.info(f"Start at : {start_time}, until : {end_time}")

    try:
        schedule.every().day.at(start_time).do(main1)
        schedule.every(10).seconds.do(repetition_work)
        # schedule.every(10).seconds.do(repetition_work)

        while True:
            schedule.run_pending()
            time.sleep(0.2)

    except Exception as ex:
        logging.error(traceback.format_exc())
        log_print(f"error {ex}")
        bot.send_telegram_message(f"exception raised: {traceback.format_exc()}")


def repetition_work():
    """
    반복작업 함수
    loop돌기[대출잔고,현재잔고 확인 > 미처리사유확인]

    """
    global main_job_done
    global start_t, end_t

    logger.debug(f"check main job done : {main_job_done} start : {start_t}, end : {end_t}")
    log_print(f"check main job done : {main_job_done} start : {start_t}, end : {end_t}")
    if not main_job_done:
        log_print("main job not done")
        logger.debug("main job not done")
        return

    now = datetime.now().strftime("%H:%M")

    if not (start_t <= now <= end_t):
        log_print("not repeat time")
        logger.debug("not repeat time")
        return


    logger.info("start repetition")
    # find_balance(8655)

    work = 반복작업(step=step, image_path=image_path)

    work.find_balance()
    result = work.get_loan_balance()

    if result.empty:
        logger.info("result_loan is empty")
    else:
        dfi.export(result, 'result_loan.png')


        bot.send_telegram_photo('result_loan')


    result2 = work.get_balance()

    if result2.empty:
        logger.info("result_balance is empty")

    else:
        dfi.export(result2,'result_balance.png')

        bot.send_telegram_photo('result_balance')

    logger.info("start unprocessed_reason")
    work.unprocessed_reason()

def main1():
    """
    연속조회부터 미처리사유작업까지 싸이클 한바퀴 돌기

    :return: 기준가 데이터 받기, 잔고확인, 미처리사유 비밀번호작성 및 사유확인, 텔레그램 메세지 발송
    """
    logger.info("start main1")
    log_print("start main1")

    once = 기본환경설정(image_path = image_path, win_name="8733")
    work = 반복작업(step=step, image_path=image_path)

    once.find_inquiry()

    once.pyauto_click_type_sleep(x=128,y=63,typing='8655',sleep_sec=2)
    once.pyauto_click_type_sleep(x=128, y=63, typing='8733', sleep_sec=2)
    once.drag_window("8733_active.png", "8655.png")
    work.find_balance()
    result_loan = work.get_loan_balance()

    if result_loan.empty:
        logger.info("result_loan is empty")
    else:
        dfi.export(result_loan, 'result_loan.png')

        bot.send_telegram_photo('result_loan')

    result_balance = work.get_balance()

    if result_balance.empty:
        logger.info("result_balance is empty")

    else:
        dfi.export(result_balance, 'result_balance.png')

        bot.send_telegram_photo('result_balance')

    logger.info("start write password")
    once.write_password("8733.png")

    logger.info("start unprocessed_reason")
    work.unprocessed_reason()

    global main_job_done
    main_job_done = True
    logger.info("main job done")
    log_print("main job done")


if __name__ == "__main__":
    main1()