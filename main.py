import WeiBanAPI
import json
import time  # time.sleep延时
import os  # 兼容文件系统
import random

tenantCode = '51900002'  # 吉珠院校ID


# 密码登录，已经失效
def pwLogin():
    print(
        '默认院校为吉林大学珠海学院，ID:' + tenantCode + '\n'
        + '若有需要，请自行抓包获取院校ID修改' + '\n'
    )

    # 登录信息输入
    account = input('请输入账号\n')
    password = input('请输入密码\n')

    # 获取Cookies
    print('\n获取Cookies中')
    cookie = WeiBanAPI.getCookie()
    print('Cookies获取成功')
    time.sleep(2)

    randomTimeStamp = random.randint(1E8, 1E12)
    print('验证码,浏览器打开 https://weiban.mycourse.cn/pharos/login/randImage.do?time=' + str(randomTimeStamp))

    verifyCode = input('请输入验证码')

    # 登录请求
    loginResponse = WeiBanAPI.login(account, password, tenantCode, randomTimeStamp, verifyCode, cookie)
    return loginResponse


def main():
    # 显示License
    licenseFile = open('.' + os.sep + 'LICENSE', encoding='utf-8')
    print(licenseFile.read())
    licenseFile.close()

    # 登录
    # loginResponse = pwLogin()
    # 补打空cookie
    cookie = ''

    loginResponse = WeiBanAPI.qrLogin()

    ### Gobal
    userProjectId = ''
    userId = ''
    ###

    try:
        print('登录成功，userName:' + loginResponse['data']['userName'])

        # 设置全局数据
        userProjectId = loginResponse['data']['preUserProjectId']
        userId = loginResponse['data']['userId']

        time.sleep(2)
    except BaseException:
        print('登录失败')
        print(loginResponse)  # TODO: 这里的loginResponse调用没有考虑网络错误等问题
        exit(0)

    # 请求解析并打印用户信息
    try:
        print('请求用户信息')
        stuInfoResponse = WeiBanAPI.getStuInfo(loginResponse['data']['userId'],
                                               tenantCode,
                                               cookie)
        print('用户信息：' + stuInfoResponse['data']['realName'] + '\n'
              + stuInfoResponse['data']['orgName']
              + stuInfoResponse['data']['specialtyName']
              )
        time.sleep(2)
    except BaseException:
        print('解析用户信息失败，将尝试继续运行，请注意运行异常')

    # 请求课程完成进度
    try:
        getProgressResponse = WeiBanAPI.getProgress(loginResponse['data']['preUserProjectId'],
                                                    tenantCode,
                                                    cookie)
        print('课程总数：' + str(getProgressResponse['data']['requiredNum']) + '\n'
              + '完成课程：' + str(getProgressResponse['data']['requiredFinishedNum']) + '\n'
              + '结束时间' + str(getProgressResponse['data']['endTime']) + '\n'
              + '剩余天数' + str(getProgressResponse['data']['lastDays'])
              )
        time.sleep(2)
    except BaseException:
        print('解析课程进度失败，将尝试继续运行，请注意运行异常')

    # 请求课程列表
    try:
        getListCourseResponse = WeiBanAPI.getListCourse(loginResponse['data']['preUserProjectId'],
                                                        '3',
                                                        tenantCode,
                                                        '',
                                                        cookie)
        time.sleep(2)
    except BaseException:
        print('请求课程列表失败')

    print('解析课程列表并发送完成请求')

    for i in getListCourseResponse['data']:
        print('\n----章节码：' + i['categoryCode'] + '章节内容：' + i['categoryName'])
        courseList = WeiBanAPI.getCourseListByCategoryCode(i['categoryCode'], userProjectId, userId, tenantCode)
        for j in courseList['data']:
            print('课程内容：' + j['resourceName'] + '\nuserCourseId:' + j['userCourseId'])

            if (j['finished'] == 1):
                print('已完成')
            else:
                print('发送完成请求')
                WeiBanAPI.doStudy(userProjectId, j['resourceId'], tenantCode, userId)
                WeiBanAPI.finishCourse(j['userCourseId'], tenantCode, cookie)

                delayInt = WeiBanAPI.getRandomTime()
                print('\n随机延时' + str(delayInt))
                time.sleep(delayInt)


if __name__ == '__main__':
    main()
