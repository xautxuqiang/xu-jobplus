#coding: utf-8

from jobplus.models import db,User,CompanyInfo,Job
import random

company_name1 = (u'实验楼科技公司',u'墨安科技公司',u'启发支付',u'有饭科技',u'腾讯科技',u'小米科技公司',u'星空科技购物集团',u'钉钉科技有限公司',u'蚂蚁金服科技公司',u'Alibaba科技公司',u'蚂蜂窝旅行公司',u'美团科技公司',u'豆瓣科技有限公司',u'哇哈哈饮料有限公司',u'红星月饼公司',u'途牛旅行',u'默默社交公司',u'借贷宝公司',u'网易科技有限公司',u'头条新闻')

company_site = ('www.shiyanlou.com','www.moan.com','www.qifa.com','www.youfan.com','www.tecent.com','www.xiaomi.com','www.xingkong.com','www.dingding.com','www.mayi.com','www.alibaba.com','www.mafengwo.com','www.meituan.com','www.douban.com','www.wahaha.com','www.hongxing.com','www.tuniu.com','www.momo.com','www.jixdaibao.com','www.wangyi.com','www.toutiao.com')

company_city = (u'北京',u'上海',u'广州',u'深圳',u'西安',u'成都',u'杭州')

company_tags = (u'移动互联网',u'电子商务',u'金融',u'企业服务',u'游戏',u'020',u'医疗健康',u'信息安全',u'旅游',u'数据服务')

finance_stage = (u'B轮',u'A轮',u'C轮',u'D轮',u'上市公司',u'不需要融资')

username = (u'白菜',u'黄瓜',u'菠菜',u'红萝卜',u'芹菜',u'油菜',u'油',u'白萝卜',u'土豆',u'红薯',u'辣椒',u'茄子',u'紫薯',u'洋葱',u'甘蓝',u'青笋',u'大蒜',u'山药',u'莲藕',u'包包菜')

user_email = ('549911582@qq.com','549911583@qq.com','549911584@qq.com','549911585@qq.com','549911586@qq.com','549911587@qq.com','549911588@qq.com','549911589@qq.com','549911590@qq.com','549911591@qq.com','549911592@qq.com','549911593@qq.com','549911594@qq.com','549911595@qq.com','549911596@qq.com','549911597@qq.com','549911598@qq.com','549911599@qq.com','549911532@qq.com','5499134785@qq.com')

company_scale = (u'15-50人',u'50-150人',u'150-500人',u'500-2000人')

company_tag = (u'节日礼物',u'技能培训',u'年度旅游',u'弹性工作',u'五险一金',u'打土豪分田地',u'定期体检',u'专项奖金')

company_introduction = """ 23魔方个人基因检测是全球最具性价比的个人基因检测服务。通过针对东亚人定制 70 万位点全基因组芯片，帮助每一个用户探索自己基因的奥秘。只需要提供 2ml 唾液，我们通过对你的基因信息进行 AI 分析，帮助用户认知遗传风险、身体特征、民族祖源、运动潜力、营养需求等方面的遗传密码。

传统基因检测是一份报告，而23魔方 APP 可以更好的带你探索自己的基因遗传。23魔方通过基因大数据不断挖掘更多的基因遗传信息。在23魔方 APP 可以看到自己的基因检测结果、参加在线研究问卷、收到最近的研究成果和最新项目推送。23魔方 APP 将带你进入数据化的基因世界，让你不断发现未知的自己。       

23魔方在2015年3月于成都成立，专注于面向中国人的消费级基因检测，是目前国内这一领域的领跑者。不过，用户和粉丝更喜欢称我们为"中国最会用口水测基因的公司"。

23魔方基因检测使用2毫升唾液作为样本，通过检测中心专业化的分析，可以得出祖源、遗传风险等200多项检测，还原了人体的"出厂配置”。这款产品经拥有10万付费用户，100万关注粉丝，覆盖全国所有省市自治区（含港澳台）。我们不擅长生产生物黑科技，只是一不小心就做成这样了。

消费级基因检测在中国是一个全新的事业，充满挑战和机遇。我们的出发点是基因检测，但23魔方的目标是在做一家最值得信赖的生命数据公司，立志于让生命的数据惠及每一个生命。我们之所以信心满满，是因为我们拥有一支强大并且有特色的队伍：

这是一支多元化的队伍。短短两年时间，23魔方从十人发展成近百人的团队。这个团队里有程序猿、生物屌、设计狮、网推狗…每个人都有自己的奇思妙想，在这里，你能get到的技能比谁都多；
 

这是一支年轻化的团队。平均年龄27岁，作为一家生物科技公司，没有一个90后脱发，7080也一样年轻有活力。我们信奉年轻是一种态度，意味着不断进步获取新知，跟红枣枸杞保温杯没什么关系；

这还是一支崇尚科技的团队。我们立志于打造深具科技范儿的产品，因此第一步是让自己变得科技起来。我们信奉让事实和数据说话，如果你有足够的事实和数据，老板也争不赢你。

23魔方现在已经走过B轮融资，是目前国内公开融资规模最大的消费级基因检测公司。所以，我的意思是，我们不缺钱，我们就缺你——只要你是高手，我就敢给高薪
"""



def generate_company():
    for i in range(20):
        random_2tags = (company_tags[random.randint(0,9)], company_tags[random.randint(0,9)])
        company = CompanyInfo(company_name=company_name1[i], company_intro=company_introduction, website=company_site[i], tags=','.join(company_tag), scale=company_scale[random.randint(0,3)], city=company_city[random.randint(0,6)], description=u"这句话是公司的一句话介绍，故意长点测试下", field=','.join(random_2tags), finance_stage=finance_stage[random.randint(0,5)])
        user = User(nickname=username[i], email=user_email[i], password="xqxq1994", detail=company, role=20)

        try:
            db.session.add(company)
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()

def generate_job():
    for i in range(20):
        job = Job(job_name=u"python工程师", salary_low=10, salary_high=15,  experience_requirement="1-3", degree_requirement=u"本科", work_location_city=u"成都", work_location_district=u"高新区", work_location_address=u"世纪大厦8楼301",tags="python,linux,web", company_id=i)
        try:
            db.session.add(job)
            db.session.commit()
        except:
            db.session.rollback()
            
def generate_data():
    generate_company()
    generate_job()

if __name__ == '__main__':
    generate_data()
    
