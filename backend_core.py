# -*- coding: utf-8 -*-
"""
日历APK后端核心（纯业务逻辑，前后端分离）
功能：日期计算、月份切换、日程增删查、日历矩阵生成
无任何UI依赖，可独立调用和测试
"""
import calendar
from datetime import datetime, date

class CalendarBackend:
    def __init__(self):
        # 初始化当前日期（关联系统当前日期）
        self.today = date.today()
        self.current_year = self.today.year
        self.current_month = self.today.month
        # 日程存储容器：key=日期字符串（格式：2026-01-17），value=日程内容
        self.schedule_dict = {}

    def switch_year(self, offset: int):
        """
        切换年份
        :param offset: 偏移量，1=下一年，-1=上一年
        """
        self.current_year += offset

    def switch_month(self, offset: int):
        """
        切换月份
        :param offset: 偏移量，1=下月，-1=上月
        """
        self.current_month += offset
        # 月份越界处理（12月+1→1月，1月-1→12月）
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        elif self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1

    def back_to_today(self):
        """返回今日日期，重置当前年月"""
        self.current_year = self.today.year
        self.current_month = self.today.month

    def get_calendar_matrix(self) -> list:
        """
        核心方法：生成当月日历二维数组（6行7列）
        补全前后空白日期，适配日历网格布局（周日~周六）
        :return: 二维列表，每个元素为日期（0表示空白）
        """
        # 获取当月日历（默认返回二维列表，每行对应一周）
        cal = calendar.monthcalendar(self.current_year, self.current_month)
        # 补全第一行前面的空白（使日历从周日对齐）
        first_week = cal[0]
        if first_week[0] != 0:
            cal.insert(0, [0]*7)
        # 补全最后一行后面的空白（保证日历为规整6行）
        last_week = cal[-1]
        if last_week[-1] != 0:
            cal.append([0]*7)
        return cal

    def get_current_date_str(self) -> str:
        """获取当前年月的格式化字符串（如：2026/01）"""
        return f"{self.current_year}/{self.current_month:02d}"

    def get_zodiac(self, year=None):
        """
        获取指定年份的生肖
        :param year: 年份，默认为当前年份
        :return: 生肖字符串（用于图片文件名）
        """
        if year is None:
            year = self.current_year
        
        zodiacs = ["猴", "鸡", "狗", "猪", "鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊"]
        index = year % 12
        return zodiacs[index]

    def is_today(self, day: int) -> bool:
        """判断指定日期是否为今日"""
        return day == self.today.day and \
               self.current_month == self.today.month and \
               self.current_year == self.today.year

    def add_schedule(self, day: int, content: str):
        """
        添加日程
        :param day: 日期（数字，如17）
        :param content: 日程内容
        """
        if day == 0:  # 空白格子（非当月日期）不允许添加日程
            return
        # 格式化日期为字符串作为键
        schedule_date = date(self.current_year, self.current_month, day).strftime("%Y-%m-%d")
        if content.strip():  # 过滤空内容
            self.schedule_dict[schedule_date] = content.strip()

    def del_schedule(self, day: int):
        """
        删除指定日期的日程
        :param day: 日期（数字，如17）
        """
        if day == 0:
            return
        schedule_date = date(self.current_year, self.current_month, day).strftime("%Y-%m-%d")
        if schedule_date in self.schedule_dict:
            del self.schedule_dict[schedule_date]

    def get_schedule(self, day: int) -> str:
        """
        获取指定日期的日程内容
        :param day: 日期（数字，如17）
        :return: 日程内容（空字符串表示无日程）
        """
        if day == 0:
            return ""
        schedule_date = date(self.current_year, self.current_month, day).strftime("%Y-%m-%d")
        return self.schedule_dict.get(schedule_date, "")

    def get_current_month_day(self, day: int) -> bool:
        """判断是否为当月有效日期（非补全的空白日期）"""
        return day != 0

# 后端测试代码（可独立运行验证功能）
if __name__ == "__main__":
    backend = CalendarBackend()
    print("当前年月：", backend.get_current_date_str())
    print("今日是否为17号：", backend.is_today(17))
    print("当月日历矩阵：", backend.get_calendar_matrix())
    # 测试添加/获取日程
    backend.add_schedule(17, "下午3点开会")
    print("17号日程：", backend.get_schedule(17))
    # 测试切换月份
    backend.switch_month(1)
    print("切换到下月：", backend.get_current_date_str())