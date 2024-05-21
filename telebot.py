import traceback
import asyncio
import telegram


class TeleBot:
    def __init__(self):
        telegram_token = '6952860214:AAEUUVuetpIEhsv0NMGp3wF-IaXuFsUwS6w'

        try:
            self.bot = telegram.Bot(telegram_token)
        except :
            traceback.print_exc()

    async def send_telegram_message(self, text):
        """
        telegram으로 메세지 발송하기
        :param text: 보내고 싶은 메세지
        :return: 텔레그램전송
        """
        telegram_id = '-1002074418471'
        try:
            res = await self.bot.send_message(chat_id=telegram_id,
                                         text=text)
        # ---------------------------------------------
        # 모든 함수의 공통 부분(Exception 처리)
        # ---------------------------------------------
        except Exception:
            raise Exception

    async def send_telegram_photo(self, image):

        telegram_id = '-1002074418471'

        try:
            res = await self.bot.send_photo(chat_id=telegram_id,
                                                 photo=open(f'C:/Users/soun/Desktop/nh_click/{image}.png', 'rb'))

            return res

        # ---------------------------------------------
        # 모든 함수의 공통 부분(Exception 처리)
        # ---------------------------------------------
        except Exception:
            raise