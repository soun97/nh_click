import logging
import traceback
import time
import pandas as pd
import pyautogui
from configparser import ConfigParser

formater = logging.Formatter("%(asctime)s - [%(filename)s:%(lineno)d] %(levelname)s -> %(message)s")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(filename)s:%(lineno)d] %(levelname)s -> %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.addHandler(logging.StreamHandler())
fileHandler = logging.FileHandler("test.log")
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(formater)
logger.addHandler(fileHandler)


class UIWork:
    def __init__(self, image_path):
        self.image_path = image_path

    def image_click_and_move(self,image_file_name, move_x, move_y, duration=0.5, sleep_sec=0.3):
        logger.debug(f"image_click_and_move - {self.image_path}/{image_file_name}")
        image_position = pyautogui.locateOnScreen(f"{self.image_path}/{image_file_name}")
        image_center = pyautogui.center(image_position)
        time.sleep(sleep_sec)
        pyautogui.click(image_center)
        pyautogui.move(move_x, move_y, duration=duration)
        return image_center


class 반복작업:

    def __init__(self, step=30, image_path=""):
        self.image_path = image_path
        self.path ="C:\\Users\\soun\\Desktop\\nh_click\\"
        self.step = step
        self.uiwork = UIWork(image_path)

    def save_csv(self,file_name):

        success = False
        attempts = 0
        max_attempts = 5

        while not success and attempts < max_attempts:
            try:
                time.sleep(0.1)
                pyautogui.rightClick()
                time.sleep(0.5)
                # csv저장클릭
                self.uiwork.image_click_and_move("save_csv.png", 0, 0, sleep_sec=0)
                success = True
                time.sleep(0.5)
                pyautogui.typewrite(f'{self.path}{file_name}')
                pyautogui.press('enter')
                logger.info(f"{file_name} file saved")
                time.sleep(0.2)
            except Exception as ex:
                attempts += 1
                logger.error(ex)
                traceback.print_exc()
        if not success:
            logger.error(f"Failed after {attempts} attempts")


    def find_balance(self):
        self.try_click_move_image(8655)
        self.save_csv("balance.csv")

    def try_click_move_image(self, win_num):

        try:
            time.sleep(0.3)
            self.uiwork.image_click_and_move(f"{win_num}.png", 0, 200, sleep_sec=3)

        except pyautogui.ImageNotFoundException:
            time.sleep(0.3)
            self.uiwork.image_click_and_move(f"{win_num}_active.png", 0, 200, sleep_sec=3)

    def unprocessed_reason(self):
        self.try_click_move_image(8733)
        self.save_csv("unprocessed_reason.csv")

    def merge_file(self):
        logger.info("start merge files")
        # -------------------------------------------------------
        # balance, inquiry file filtering
        # ------------------------------------------------------
        balance_df = pd.read_csv(f'{self.path}balance.csv', encoding='cp949')
        new_balance = balance_df[['종목코드', '종목명', '구분', '잔고수량']]
        inquiry_df = pd.read_csv(f'{self.path}inquiry.csv', encoding='cp949')
        new_inquiry = inquiry_df[['종목코드', '종목명', '기준수량']]

        # 서버실 컴퓨터에서는 필요 없는 코드 > inquiry 타입 비교해서 타입변경하기(수정)
        if new_inquiry['종목코드'].dtype != 'str':
            new_inquiry['종목코드'] = new_inquiry['종목코드'].fillna(-1).astype('int').astype('str')

        if new_balance['종목코드'].dtype != 'str':
            new_balance['종목코드'] = new_balance['종목코드'].fillna(-1).astype('int').astype('str')

        # -------------------------------------------------------
        # merge & calculate :설정상환단계보다 현금보유량이 낮으면 알림
        # ------------------------------------------------------
        merge = pd.merge(left=new_balance, right=new_inquiry, how='outer', on='종목코드')
        merge[f'기준가*{self.step}'] = merge['기준수량'] * int(self.step)
        merge = merge.dropna()
        merge['잔고수량'] = merge['잔고수량'].str.replace(",", "").astype('int')
        return merge

    def get_loan_balance(self):
        # -------------------------------------------------------
        # balance, inquiry file filtering : 대출보유 종목 중 현재 잔고 기준수량 이하인 종목
        # ------------------------------------------------------
        merge = self.merge_file()
        담보 = merge[merge['구분'] == '대출담보']
        현금 = merge[merge['구분'] == '현금']
        merge2 = pd.merge(담보, 현금, left_on='종목코드', right_on='종목코드', how='left', suffixes=('_대출', '_현금'))
        result = merge2[merge2['잔고수량_현금'] < merge2[f'기준가*{self.step}_현금']]
        return result

    def get_balance(self):
        """
        대출 보유하고 있지 않은 종목 중 현재 잔고 수량이 0인 것
        :return: 현재잔고 0인 종목
        """
        merge = self.merge_file()
        filtered_df = merge.groupby('종목명_x').filter(lambda x: (x['구분'] == '현금').all())
        empty_balance = filtered_df[filtered_df['잔고수량'] == 0]
        empty_balance = pd.DataFrame(empty_balance)
        return empty_balance


class 기본환경설정:

    def __init__(self,image_path,win_name):
        self.image_path = image_path
        self.win_name = win_name
        self.x = 133
        self.y = 63
        self.path ="C:\\Users\\soun\\Desktop\\nh_click\\"
        self.uiwork = UIWork(image_path)

    def write_password(self,win_name):
        logger.debug(f"{self.image_path}/{win_name}")
        unprocessed = pyautogui.locateOnScreen(f"{self.image_path}/{win_name}")
        unprocessed_center = pyautogui.center(unprocessed)
        pyautogui.click(unprocessed_center)
        pyautogui.press('enter')
        pyautogui.typewrite('vhfptmxm')

    def new_connection(self):
        try:
            connection_error=pyautogui.locateOnScreen(f"{self.image_path}/new_connection.png")
            connection_center = pyautogui.center(connection_error)
            pyautogui.click(connection_center)
            time.sleep(0.1)

            pyautogui.press('tab')
            time.sleep(0.1)
            pyautogui.press('tab')
            time.sleep(0.1)
            pyautogui.press('space')
            time.sleep(0.1)
            pyautogui.press('enter')

        except Exception as ex:
            traceback.print_exc()

    def find_inquiry(self):

        success=False
        retry_count = 0
        while not success and retry_count<3:
            try:
                self.pyauto_click_type_sleep(x=self.x,y=self.y,typing="8729",sleep_sec=0.8)
                inquiry_center = self.uiwork.image_click_and_move("8729.png", 50, 200)

                t3 = 반복작업()
                t3.save_csv("inquiry.csv")
                success = True

            except Exception as ex:
                self.new_connection()
                retry_count += 1

        if not success:
                logger.error(ex)
                traceback.print_exc()


    def drag_window(self,image_path1, image_path2):

        try:
            self.uiwork.image_click_and_move(image_path1, 0, 0, sleep_sec=0)
            time.sleep(2)
            pyautogui.dragTo(1300, 0, duration=0.5)
        except pyautogui.ImageNotFoundException:
            # log or print the exception
            logger.info(f'image "{image_path1}" not found. Trying alternative image.')
            self.uiwork.image_click_and_move(image_path2, 0, 0, sleep_sec=0)
            time.sleep(2)
            pyautogui.dragTo(1300, 0, duration=0.5)


    def pyauto_click_type_sleep(self, x, y, typing, sleep_sec):
        pyautogui.click(x=x, y=y)
        pyautogui.typewrite(typing)
        time.sleep(sleep_sec)




if __name__ == "__main__":
    config = ConfigParser()
    config.read("config.ini")
    image_path = config["images"]["dir"]

    c = 기본환경설정(image_path=image_path, win_name="8733")
    # c.find_inquiry(save_name="inquiry")
    # time.sleep(2)
    # c.pyauto_click_type_sleep(x=128, y=63, typing="8655", sleep_sec=2)
    # c.pyauto_click_type_sleep(x=128, y=63, typing="8733", sleep_sec=2)
    # c.drag_window("8733_active.png", "8655.png")
    # c.write_password("8733.png")

    w = 반복작업(step=40, image_path=image_path)
    # w.find_balance()
    time.sleep(0.5)

    loan_balance = w.get_loan_balance()
    print("loan balance : ", loan_balance)