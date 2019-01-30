#爬斗鱼主播名字和观众数量小案例--自动化测试工具
import unittest
from selenium import webdriver
from bs4 import BeautifulSoup as bs

class Douyu(unittest.TestCase):
    # 初始化方法，必须是setUp()
    def setUp(self):
        self.driver = webdriver.PhantomJS()
        self.num = 0

    # 测试方法必须有test字样开头
    def testDouyu(self):
        self.driver.get("https://www.douyu.com/directory/all")

        while True:
            soup = bs(self.driver.page_source, "lxml")
            # 房间名, 返回列表
            names = soup.find_all("h3", {"class" : "ellipsis"})
            # 观众人数, 返回列表
            numbers = soup.find_all("span", {"class" :"dy-num fr"})
            #第几页
            page_nums = soup.find_all("a", {"class": "shark-pager-item current"})
            #直播链接，返回列表
            links = soup.find_all("a",{"class":"play-list-link"})

            for num in page_nums:
                page_num = num.get_text()

            print("第"+page_num+"页")

            # zip(names,numbers,links) 将name、number和links这三个列表合并为一个元组 : [(1, 2，3), (4，5, 6)...]
            for name,number,link in zip(names,numbers,links):
                str = u"观众人数: " + number.get_text().strip() + u"\t房间名: " + name.get_text().strip()+ u"\t直播链接: " +"https://www.douyu.com"+link.get("href").strip()
                print('%s'%str)
                self.num += 1

            # 如果在页面源码里找到"下一页"为隐藏的标签，就退出循环
            if int(page_num) >= 10:
                break

            # 一直点击下一页
            self.driver.find_element_by_class_name("shark-pager-next").click()

    # 测试结束执行的方法
    def tearDown(self):
        # 退出PhantomJS()浏览器
        print("当前网站前十页直播人数" + str(self.num))
        self.driver.quit()

if __name__ == "__main__":
    # 启动测试模块
    unittest.main()

