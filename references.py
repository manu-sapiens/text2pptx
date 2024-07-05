INSTRUCTION_30_REFS = '''
Leveraging the resume of the user found in the RESUME section, curate a list of 30 suggested resources most relevant to the JOB_DESCRIPTION, arranged in groups of 5 sources each, to help the user bridge their KNOWLEDGE GAP.  
Please output your list of 30 resources with a clear category header for each of the groups as a json following the provided json schema.
'''

GPT_TOOL_SCHEMA_30_REFS = '''
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "GroupedFinancialResources",
  "type": "object",
  "properties": {
    "categories": {
      "type": "array",
      "description": "An array of categories, each containing a title and a list of financial resource URLs with metadata.",
      "items": {
        "type": "object",
        "properties": {
          "category": {
            "type": "string",
            "description": "The title of the category."
          },
         "gap":{
            "type": "string",
            "description": "The specific gap the candidate needs to overcome."},
         "explanation": {
            "type": "string",
            "description": "Explain how these resources will help the candidate overcome a specific gap."
          },          
          "sources": {
            "type": "array",
            "description": "An array of financial resource URLs with metadata.",
            "items": {
              "type": "string",
              "description": "A URL from the provided financial resources, appended with the type, title, and description as query parameters.",
              "enum": [
                "https://www.wallstreetoasis.com/resources/interviews/investment-banking-interview-questions-answers?type=Investment_Banking_Resources&title=101%20Investment%20Banking%20Interview%20Questions&description=Provides%20a%20comprehensive%20list%20of%20interview%20questions%20commonly%20asked%20in%20investment%20banking%20interviews.",
                "https://www.streetofwalls.com/finance-training-courses/investment-banking-overview-and-behavioral-training/investment-banking-overview?type=Investment_Banking_Resources&title=Investment%20Banking%20Hierarchy&description=Explains%20the%20various%20roles%20and%20structures%20within%20an%20investment%20bank.",
                "https://mergersandinquisitions.com/investment-banking-interview-questions-and-answers/?type=Investment_Banking_Resources&title=Investment%20Banking%20Interview%20Questions%20and%20Answers%3A%20The%20Definitive%20Guide&description=A%20detailed%20guide%20that%20covers%20potential%20questions%20and%20answers%20for%20investment%20banking%20interviews.",
                "https://mergersandinquisitions.com/investment-banking/recruitment/resumes/?type=Investment_Banking_Resources&title=Investment%20Banking%20Resumes&description=Offers%20tips%20and%20examples%20for%20crafting%20an%20effective%20resume%20for%20investment%20banking%20roles.",
                "https://mergersandinquisitions.com/how-to-get-into-investment-banking/#HowToGetIn?type=Investment_Banking_Resources&title=How%20to%20get%20into%20Investment%20Banking&description=Provides%20strategies%20and%20steps%20for%20breaking%20into%20the%20investment%20banking%20industry.",
                "https://www.wallstreetprep.com/knowledge/ma-analyst-day-in-the-life/?type=Investment_Banking_Resources&title=Day%20in%20the%20Life%20of%20an%20IB%20analyst&description=Describes%20a%20typical%20day%20for%20an%20investment%20banking%20analyst%2C%20offering%20insights%20into%20the%20daily%20tasks%20and%20work%20environment.",
                "https://www.investopedia.com/articles/financialcareers/10/investment-banking-interview.asp?type=Investment_Banking_Resources&title=What%20To%20Know%20for%20an%20Investment%20Banking%20Interview&description=Discusses%20key%20topics%20and%20knowledge%20areas%20relevant%20for%20investment%20banking%20interviews.",
                "https://corporatefinanceinstitute.com/resources/career/real-investment-banking-interview-questions-form/?type=Investment_Banking_Resources&title=More%20IB%20interview%20q%26a&description=Collection%20of%20real%20interview%20questions%20and%20answers%20for%20investment%20banking%20job%20candidates.",
                "https://igotanoffer.com/blogs/finance/investment-banking-interview-prep?type=Investment_Banking_Resources&title=Investment%20banking%20interview%20prep%20guide&description=A%20guide%20to%20preparing%20for%20investment%20banking%20interviews%2C%20including%20tips%20on%20how%20to%20answer%20common%20questions.",
                "https://www.indeed.com/career-advice/interviewing/investment-bank-interview-questions?type=Investment_Banking_Resources&title=IB%20interview%20sample%20questions&description=Sample%20questions%20that%20may%20be%20asked%20during%20an%20investment%20banking%20interview%2C%20with%20guidance%20on%20how%20to%20respond.",
                "https://www.streetofwalls.com/articles/private-equity/learn-the-basics/how-private-equity-works/?type=Private_Equity_Resources&title=How%20a%20PE%20Firm%20Works&description=Explains%20the%20fundamental%20operations%20of%20a%20private%20equity%20firm.",
                "https://mergersandinquisitions.com/private-equity/recruitment/?type=Private_Equity_Resources&title=How%20to%20Break%20into%20Private%20Equity&description=Provides%20strategies%20for%20securing%20a%20position%20in%20the%20private%20equity%20sector.",
                "https://www.streetofwalls.com/finance-training-courses/private-equity-training/private-equity-resume/?type=Private_Equity_Resources&title=PE%20Resume&description=Offers%20guidance%20on%20crafting%20a%20resume%20tailored%20for%20private%20equity%20roles.",
                "https://www.wallstreetoasis.com/resources/interviews/private-equity-interview-questions?type=Private_Equity_Resources&title=PE%20Interview%20Questions&description=Features%20a%20list%20of%20common%20interview%20questions%20asked%20during%20PE%20interviews.",
                "https://mergersandinquisitions.com/private-equity-interviews/?type=Private_Equity_Resources&title=Private%20Equity%20Interviews%20101%3A%20How%20to%20Win%20Offers&description=Provides%20a%20guide%20to%20excelling%20in%20private%20equity%20interviews.",
                "https://mergersandinquisitions.com/private-equity/?type=Private_Equity_Resources&title=Private%20Equity%20Overview&description=An%20overview%20of%20the%20private%20equity%20industry%2C%20including%20key%20practices%20and%20challenges.",
                "https://www.wallstreetprep.com/knowledge/lbo-modeling-test-example-solutions/?type=Private_Equity_Resources&title=Basic%20LBO%20Modelling%20Test&description=Introduces%20a%20basic%20leveraged%20buyout%20%28LBO%29%20modeling%20test%20with%20example%20solutions.",
                "https://www.wallstreetprep.com/knowledge/leveraged-buyout-lbo-modeling-1-hour-practice-test/?type=Private_Equity_Resources&title=Standard%20LBO%20Modelling%20Test&description=Provides%20a%20practice%20LBO%20modeling%20test%20designed%20to%20be%20completed%20within%20one%20hour.",
                "https://www.wallstreetprep.com/knowledge/advanced-lbo-modeling-test-4-hour-example/?type=Private_Equity_Resources&title=Advanced%20LBO%20Modelling%20Test&description=Features%20an%20advanced%20LBO%20modeling%20test%20that%20spans%20four%20hours%2C%20intended%20for%20more%20experienced%20professionals.",
                "https://growthequityinterviewguide.com/private-equity-interview-questions?type=Private_Equity_Resources&title=Top%2017%20PE%20Interview%20Questions&description=Lists%20top%2017%20interview%20questions%20specific%20to%20private%20equity%20interviews.",
                "https://www.fe.training/free-resources/careers-in-finance/private-equity-interview-questions/?type=Private_Equity_Resources&title=More%20PE%20Interview%20Questions&description=A%20collection%20of%20additional%20private%20equity%20interview%20questions.",
                "https://readwrite.com/the-art-of-private-equity-interviewing-tips-for-impressive-responses/?type=Private_Equity_Resources&title=Tips%20for%20Impressive%20Responses%20for%20PE%20Interview&description=Offers%20tips%20on%20how%20to%20deliver%20impressive%20responses%20in%20private%20equity%20interviews.",
                "https://transacted.io/private-equity-interview-preparation-guide/?type=Private_Equity_Resources&title=PE%20Interview%20Prep%20Guide&description=A%20comprehensive%20guide%20to%20preparing%20for%20private%20equity%20interviews.",
                "https://www.10xebitda.com/why-private-equity-interview-answer/?type=Private_Equity_Resources&title=How%20to%20Answer%20%E2%80%98Why%20Private%20Equity%E2%80%99&description=Provides%20insights%20on%20how%20to%20effectively%20answer%20common%20questions%20about%20one%27s%20motivation%20for%20pursuing%20a%20career%20in%20private%20equity.",
                "https://www.wallstreetoasis.com/resources/interviews/venture-capital-interview-questions?type=Venture_Capital_Resources&title=VC%20Interview%20Questions&description=A%20list%20of%20common%20questions%20asked%20during%20venture%20capital%20interviews.",
                "https://mergersandinquisitions.com/venture-capital?type=Venture_Capital_Resources&title=VC%20Overview&description=Provides%20a%20broad%20overview%20of%20the%20venture%20capital%20industry%2C%20including%20key%20players%20and%20processes.",
                "https://mergersandinquisitions.com/venture-capital-interview-questions?type=Venture_Capital_Resources&title=Venture%20Capital%20Interview%20Questions%3A%20What%20to%20Expect%20and%20How%20to%20Prepare&description=Detailed%20guide%20on%20what%20to%20expect%20in%20VC%20interviews%20and%20how%20to%20prepare%20effectively.",
                "https://www.wallstreetprep.com/knowledge/venture-capital-diligence/?type=Venture_Capital_Resources&title=Fundamentals%20of%20Early-Stage%20Investing&description=Explains%20the%20due%20diligence%20process%20in%20early-stage%20venture%20capital%20investing.",
                "https://www.investopedia.com/articles/financial-careers/08/venture-capital-interview-questions.asp?type=Venture_Capital_Resources&title=Top%20VC%20Interview%20Questions&description=Outlines%20some%20of%20the%20top%20interview%20questions%20for%20venture%20capital%20job%20applicants.",
                "https://www.goingvc.com/post/the-ultimate-venture-capital-interview-guide?type=Venture_Capital_Resources&title=Ultimate%20VC%20Interview%20Guide&description=Comprehensive%20guide%20to%20succeeding%20in%20venture%20capital%20interviews.",
                "https://www.joinleland.com/library/a/50-most-common-venture-capital-interview-questions?type=Venture_Capital_Resources&title=50%20Most%20Common%20VC%20Interview%20Questions&description=Compiles%20the%2050%20most%20frequently%20asked%20questions%20in%20VC%20interviews.",
                "https://sg.indeed.com/career-advice/interviewing/venture-capital-interview-questions?type=Venture_Capital_Resources&title=37%20VC%20Interview%20Questions%20with%20Answers&description=Provides%20a%20set%20of%2037%20venture%20capital%20interview%20questions%20along%20with%20suggested%20answers.",
                "https://www.wallstreetoasis.com/resources/interviews/hedge-funds-interview-questions?type=Hedge_Fund_Resources&title=Hedge%20Fund%20Interview%20Questions&description=A%20collection%20of%20common%20interview%20questions%20faced%20during%20hedge%20fund%20interviews.",
                "https://www.wallstreetprep.com/knowledge/hedge-fund?type=Hedge_Fund_Resources&title=Hedge%20Fund%20Primer&description=An%20introductory%20guide%20to%20understanding%20the%20basic%20concepts%20and%20strategies%20of%20hedge%20funds.",
                "https://mergersandinquisitions.com/how-to-get-a-job-at-a-hedge-fund/?type=Hedge_Fund_Resources&title=How%20to%20Get%20a%20Job%20at%20a%20Hedge%20Fund&description=Detailed%20strategies%20and%20advice%20for%20landing%20a%20job%20in%20the%20hedge%20fund%20industry.",
                "https://www.streetofwalls.com/articles/hedge-fund/?type=Hedge_Fund_Resources&title=Articles%20on%20Hedge%20Funds&description=A%20compilation%20of%20various%20articles%20providing%20in-depth%20insights%20into%20the%20hedge%20fund%20industry.",
                "https://www.wallstreetmojo.com/hedge-fund-interview-questions/?type=Hedge_Fund_Resources&title=Top%2020%20HF%20Interview%20Q%26A&description=Top%2020%20questions%20and%20answers%20to%20expect%20in%20a%20hedge%20fund%20interview.",
                "https://www.daytrading.com/hedge-fund-interview-questions?type=Hedge_Fund_Resources&title=More%20HF%20Interview%20Q%26A&description=Additional%20hedge%20fund%20interview%20questions%20that%20could%20be%20crucial%20for%20candidates.",
                "https://uk.indeed.com/career-advice/interviewing/hedge-fund-interview-questions?type=Hedge_Fund_Resources&title=40%20Hedge%20Fund%20Interview%20Questions%20%28with%20Sample%20Answers%29&description=A%20robust%20list%20of%2040%20hedge%20fund%20interview%20questions%20along%20with%20guidance%20on%20sample%20answers.",
                "https://www.selbyjennings.com/blog/2023/05/preparing-for-a-hedge-fund-interview-your-comprehensive-guide?type=Hedge_Fund_Resources&title=How%20to%20Prepare%20for%20a%20HF%20Interview&description=A%20comprehensive%20guide%20to%20preparing%20for%20hedge%20fund%20interviews%2C%20covering%20what%20to%20know%20and%20how%20to%20present%20oneself.",
                "https://www.efinancialcareers.sg/news/2023/05/hedge-fund-interview-questions?type=Hedge_Fund_Resources&title=Hedge%20Fund%20Interview%20Questions%3A%20What%20to%20Expect%2C%20and%20What%20to%20Ask&description=Insight%20into%20what%20candidates%20can%20expect%20to%20face%20in%20hedge%20fund%20interviews%20and%20suggestions%20on%20what%20questions%20to%20ask.",
                "https://www.buysidehustle.com/most-frequently-asked-hedge-fund-interview-questions-and-answers/?type=Hedge_Fund_Resources&title=Most%20Frequently%20Asked%20HF%20Interview%20Questions&description=Lists%20the%20most%20frequently%20asked%20questions%20in%20hedge%20fund%20interviews%2C%20complete%20with%20answers.",
                "https://www.wallstreetoasis.com/resources/interviews/accounting-interview-questions?type=Accounting_Resources&title=Accounting%20Interview%20Questions&description=A%20list%20of%20common%20questions%20asked%20during%20accounting%20interviews.",
                "https://www.wallstreetprep.com/knowledge/operating-cash-flow-ocf/?type=Accounting_Resources&title=Fundamentals%20of%20Free%20Cash%20Flow%20%28FCF%29&description=Explains%20the%20basics%20of%20calculating%20and%20analyzing%20free%20cash%20flow%2C%20an%20essential%20concept%20in%20accounting%20and%20finance.",
                "https://www.robertwalters.co.uk/insights/career-advice/blog/five-accounting-interview-tips.html?type=Accounting_Resources&title=Tips%20for%20Accounting%20Interview&description=Provides%20practical%20tips%20to%20excel%20in%20accounting%20interviews%2C%20focusing%20on%20how%20to%20present%20technical%20knowledge%20and%20soft%20skills.",
                "https://www.shiksha.com/online-courses/articles/top-accounting-interview-questions-answers/?type=Accounting_Resources&title=Top%20128%20Accounting%20Interview%20Q%26A&description=A%20comprehensive%20list%20of%20accounting%20interview%20questions%20and%20answers%2C%20covering%20a%20wide%20range%20of%20topics%20in%20the%20field.",
                "https://www.franklin.edu/blog/accounting-mvp/accounting-interview-questions?type=Accounting_Resources&title=How%20to%20Prepare%20for%20Accounting%20Interview&description=Discusses%20strategies%20to%20prepare%20for%20an%20accounting%20interview%2C%20including%20understanding%20what%20recruiters%20are%20looking%20for.",
                "https://accountingsoftwareanswers.com/accounting-interview-questions/?type=Accounting_Resources&title=Guide%20for%20an%20Accounting%20Interview&description=A%20guide%20to%20preparing%20for%20accounting%20interviews%2C%20offering%20insights%20into%20the%20types%20of%20questions%20and%20how%20to%20answer%20them%20effectively.",
                "https://www.sienaheights.edu/how-to-prepare-for-accounting-interview-questions/?type=Accounting_Resources&title=How%20to%20Prepare%20for%20Accounting%20Interview%20Questions&description=Provides%20a%20detailed%20approach%20to%20preparing%20for%20accounting%20interviews%2C%20emphasizing%20the%20importance%20of%20practical%20examples%20to%20illustrate%20accounting%20skills.",
                "https://www.remoterocketship.com/advice/6-risk-analyst-interview-questions-with-sample-answers?type=Risk_Analyst_Resources&title=6%20Risk%20Analyst%20Interview%20Questions%20with%20Sample%20Answers&description=This%20page%20provides%20a%20curated%20list%20of%20interview%20questions%20specifically%20for%20risk%20analyst%20positions%20along%20with%20detailed%20sample%20answers%20to%20help%20candidates%20prepare%20effectively.",
                "https://www.investopedia.com/articles/professionals/111115/common-interview-questions-credit-risk-analysts.asp?type=Risk_Analyst_Resources&title=Common%20Interview%20Questions%3A%20Credit%20Risk%20Analysts&description=Investopedia%20outlines%20common%20interview%20questions%20faced%20by%20credit%20risk%20analysts%2C%20offering%20insights%20into%20the%20skills%20and%20knowledge%20expected%20in%20the%20role.",
                "https://www.ziprecruiter.com/career/job-interview-question-answers/risk-analyst?type=Risk_Analyst_Resources&title=Top%2015%20Risk%20Analyst%20Job%20Interview%20Questions%2C%20Answers%20%26%20Tips&description=ZipRecruiter%20presents%20a%20list%20of%20top%20interview%20questions%20for%20risk%20analysts%2C%20including%20tips%20on%20how%20to%20answer%20and%20what%20employers%20are%20looking%20for.",
                "https://www.indeed.com/career-advice/finding-a-job/how-to-become-risk-analyst?type=Risk_Analyst_Resources&title=How%20To%20Become%20a%20Risk%20Analyst%3A%206%20Steps&description=Indeed%20guides%20on%20the%20steps%20to%20becoming%20a%20risk%20analyst%2C%20detailing%20necessary%20education%2C%20skills%2C%20and%20career%20paths.",
                "https://www.theknowledgeacademy.com/blog/risk-management-interview-questions/?type=Risk_Analyst_Resources&title=Top%2040%20Risk%20Management%20Interview%20Questions&description=The%20Knowledge%20Academy%20provides%20a%20comprehensive%20list%20of%20risk%20management%20interview%20questions%20to%20help%20candidates%20prepare%20for%20interviews%20in%20risk%20management%20roles.",
                "https://www.projectpro.io/article/financial-data-scientist/925?type=IT_Resources&title=How%20to%20Become%20a%20Financial%20Data%20Scientist&description=This%20article%20outlines%20the%20initial%20steps%20necessary%20to%20pursue%20a%20career%20as%20a%20financial%20data%20scientist%2C%20emphasizing%20the%20importance%20of%20mastering%20statistical%20concepts%20and%20analytical%20skills.",
                "https://onlinedegrees.sandiego.edu/data-science-in-finance/?type=IT_Resources&title=Data%20Science%20in%20Finance%20%5BCareer%20Guide%5D&description=The%20guide%20explores%20the%20role%20of%20data%20science%20in%20the%20finance%20sector%2C%20detailing%20the%20skills%20required%20and%20the%20impact%20of%20data%20science%20on%20financial%20strategies%20and%20decisions.",
                "https://www.jobzmall.com/careers/financial-data-scientist/faqs/how-can-i-best-prepare-for-a-career-as-a-financial-data-scientist?type=IT_Resources&title=How%20can%20I%20best%20prepare%20for%20a%20career%20as%20a%20Financial%20Data%20Scientist%3F&description=This%20FAQ%20section%20provides%20insights%20into%20the%20preparations%20necessary%20for%20a%20career%20as%20a%20financial%20data%20scientist%2C%20with%20tips%20on%20education%2C%20skills%20development%2C%20and%20practical%20experience."
              ]
            }
          }
        },
        "required": ["category", "sources"]
      }
    }
  },
  "required": ["categories"]
}
'''

GPT_TOOL_SCHEMA_FINANCIAL_REFERENCES = '''
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "FinancialResourceRecommendation",
  "type": "object",
  "properties": {
    "recommendation": {
      "type": "string",
      "description": "A recommendation of a financial resource with an explanation of why this resource was chosen."
    },
    "reference_url": {
      "type": "string",
      "description": "A URL from the provided financial resources, appended with the type, title, and description as query parameters.",
      "enum": [
        "https://www.wallstreetoasis.com/resources/interviews/investment-banking-interview-questions-answers?type=Investment_Banking_Resources&title=101%20Investment%20Banking%20Interview%20Questions&description=Provides%20a%20comprehensive%20list%20of%20interview%20questions%20commonly%20asked%20in%20investment%20banking%20interviews.",
        "https://www.streetofwalls.com/finance-training-courses/investment-banking-overview-and-behavioral-training/investment-banking-overview?type=Investment_Banking_Resources&title=Investment%20Banking%20Hierarchy&description=Explains%20the%20various%20roles%20and%20structures%20within%20an%20investment%20bank.",
        "https://mergersandinquisitions.com/investment-banking-interview-questions-and-answers/?type=Investment_Banking_Resources&title=Investment%20Banking%20Interview%20Questions%20and%20Answers%3A%20The%20Definitive%20Guide&description=A%20detailed%20guide%20that%20covers%20potential%20questions%20and%20answers%20for%20investment%20banking%20interviews.",
        "https://mergersandinquisitions.com/investment-banking/recruitment/resumes/?type=Investment_Banking_Resources&title=Investment%20Banking%20Resumes&description=Offers%20tips%20and%20examples%20for%20crafting%20an%20effective%20resume%20for%20investment%20banking%20roles.",
        "https://mergersandinquisitions.com/how-to-get-into-investment-banking/#HowToGetIn?type=Investment_Banking_Resources&title=How%20to%20get%20into%20Investment%20Banking&description=Provides%20strategies%20and%20steps%20for%20breaking%20into%20the%20investment%20banking%20industry.",
        "https://www.wallstreetprep.com/knowledge/ma-analyst-day-in-the-life/?type=Investment_Banking_Resources&title=Day%20in%20the%20Life%20of%20an%20IB%20analyst&description=Describes%20a%20typical%20day%20for%20an%20investment%20banking%20analyst%2C%20offering%20insights%20into%20the%20daily%20tasks%20and%20work%20environment.",
        "https://www.investopedia.com/articles/financialcareers/10/investment-banking-interview.asp?type=Investment_Banking_Resources&title=What%20To%20Know%20for%20an%20Investment%20Banking%20Interview&description=Discusses%20key%20topics%20and%20knowledge%20areas%20relevant%20for%20investment%20banking%20interviews.",
        "https://corporatefinanceinstitute.com/resources/career/real-investment-banking-interview-questions-form/?type=Investment_Banking_Resources&title=More%20IB%20interview%20q%26a&description=Collection%20of%20real%20interview%20questions%20and%20answers%20for%20investment%20banking%20job%20candidates.",
        "https://igotanoffer.com/blogs/finance/investment-banking-interview-prep?type=Investment_Banking_Resources&title=Investment%20banking%20interview%20prep%20guide&description=A%20guide%20to%20preparing%20for%20investment%20banking%20interviews%2C%20including%20tips%20on%20how%20to%20answer%20common%20questions.",
        "https://www.indeed.com/career-advice/interviewing/investment-bank-interview-questions?type=Investment_Banking_Resources&title=IB%20interview%20sample%20questions&description=Sample%20questions%20that%20may%20be%20asked%20during%20an%20investment%20banking%20interview%2C%20with%20guidance%20on%20how%20to%20respond.",
        "https://www.streetofwalls.com/articles/private-equity/learn-the-basics/how-private-equity-works/?type=Private_Equity_Resources&title=How%20a%20PE%20Firm%20Works&description=Explains%20the%20fundamental%20operations%20of%20a%20private%20equity%20firm.",
        "https://mergersandinquisitions.com/private-equity/recruitment/?type=Private_Equity_Resources&title=How%20to%20Break%20into%20Private%20Equity&description=Provides%20strategies%20for%20securing%20a%20position%20in%20the%20private%20equity%20sector.",
        "https://www.streetofwalls.com/finance-training-courses/private-equity-training/private-equity-resume/?type=Private_Equity_Resources&title=PE%20Resume&description=Offers%20guidance%20on%20crafting%20a%20resume%20tailored%20for%20private%20equity%20roles.",
        "https://www.wallstreetoasis.com/resources/interviews/private-equity-interview-questions?type=Private_Equity_Resources&title=PE%20Interview%20Questions&description=Features%20a%20list%20of%20common%20interview%20questions%20asked%20during%20PE%20interviews.",
        "https://mergersandinquisitions.com/private-equity-interviews/?type=Private_Equity_Resources&title=Private%20Equity%20Interviews%20101%3A%20How%20to%20Win%20Offers&description=Provides%20a%20guide%20to%20excelling%20in%20private%20equity%20interviews.",
        "https://mergersandinquisitions.com/private-equity/?type=Private_Equity_Resources&title=Private%20Equity%20Overview&description=An%20overview%20of%20the%20private%20equity%20industry%2C%20including%20key%20practices%20and%20challenges.",
        "https://www.wallstreetprep.com/knowledge/lbo-modeling-test-example-solutions/?type=Private_Equity_Resources&title=Basic%20LBO%20Modelling%20Test&description=Introduces%20a%20basic%20leveraged%20buyout%20%28LBO%29%20modeling%20test%20with%20example%20solutions.",
        "https://www.wallstreetprep.com/knowledge/leveraged-buyout-lbo-modeling-1-hour-practice-test/?type=Private_Equity_Resources&title=Standard%20LBO%20Modelling%20Test&description=Provides%20a%20practice%20LBO%20modeling%20test%20designed%20to%20be%20completed%20within%20one%20hour.",
        "https://www.wallstreetprep.com/knowledge/advanced-lbo-modeling-test-4-hour-example/?type=Private_Equity_Resources&title=Advanced%20LBO%20Modelling%20Test&description=Features%20an%20advanced%20LBO%20modeling%20test%20that%20spans%20four%20hours%2C%20intended%20for%20more%20experienced%20professionals.",
        "https://growthequityinterviewguide.com/private-equity-interview-questions?type=Private_Equity_Resources&title=Top%2017%20PE%20Interview%20Questions&description=Lists%20top%2017%20interview%20questions%20specific%20to%20private%20equity%20interviews.",
        "https://www.fe.training/free-resources/careers-in-finance/private-equity-interview-questions/?type=Private_Equity_Resources&title=More%20PE%20Interview%20Questions&description=A%20collection%20of%20additional%20private%20equity%20interview%20questions.",
        "https://readwrite.com/the-art-of-private-equity-interviewing-tips-for-impressive-responses/?type=Private_Equity_Resources&title=Tips%20for%20Impressive%20Responses%20for%20PE%20Interview&description=Offers%20tips%20on%20how%20to%20deliver%20impressive%20responses%20in%20private%20equity%20interviews.",
        "https://transacted.io/private-equity-interview-preparation-guide/?type=Private_Equity_Resources&title=PE%20Interview%20Prep%20Guide&description=A%20comprehensive%20guide%20to%20preparing%20for%20private%20equity%20interviews.",
        "https://www.10xebitda.com/why-private-equity-interview-answer/?type=Private_Equity_Resources&title=How%20to%20Answer%20%E2%80%98Why%20Private%20Equity%E2%80%99&description=Provides%20insights%20on%20how%20to%20effectively%20answer%20common%20questions%20about%20one%27s%20motivation%20for%20pursuing%20a%20career%20in%20private%20equity.",    "https://www.wallstreetoasis.com/resources/interviews/venture-capital-interview-questions?type=Venture_Capital_Resources&title=VC%20Interview%20Questions&description=A%20list%20of%20common%20questions%20asked%20during%20venture%20capital%20interviews.",
        "https://mergersandinquisitions.com/venture-capital?type=Venture_Capital_Resources&title=VC%20Overview&description=Provides%20a%20broad%20overview%20of%20the%20venture%20capital%20industry%2C%20including%20key%20players%20and%20processes.",
        "https://mergersandinquisitions.com/venture-capital-interview-questions?type=Venture_Capital_Resources&title=Venture%20Capital%20Interview%20Questions%3A%20What%20to%20Expect%20and%20How%20to%20Prepare&description=Detailed%20guide%20on%20what%20to%20expect%20in%20VC%20interviews%20and%20how%20to%20prepare%20effectively.",
        "https://www.wallstreetprep.com/knowledge/venture-capital-diligence/?type=Venture_Capital_Resources&title=Fundamentals%20of%20Early-Stage%20Investing&description=Explains%20the%20due%20diligence%20process%20in%20early-stage%20venture%20capital%20investing.",
        "https://www.investopedia.com/articles/financial-careers/08/venture-capital-interview-questions.asp?type=Venture_Capital_Resources&title=Top%20VC%20Interview%20Questions&description=Outlines%20some%20of%20the%20top%20interview%20questions%20for%20venture%20capital%20job%20applicants.",
        "https://www.goingvc.com/post/the-ultimate-venture-capital-interview-guide?type=Venture_Capital_Resources&title=Ultimate%20VC%20Interview%20Guide&description=Comprehensive%20guide%20to%20succeeding%20in%20venture%20capital%20interviews.",
        "https://www.joinleland.com/library/a/50-most-common-venture-capital-interview-questions?type=Venture_Capital_Resources&title=50%20Most%20Common%20VC%20Interview%20Questions&description=Compiles%20the%2050%20most%20frequently%20asked%20questions%20in%20VC%20interviews.",
        "https://sg.indeed.com/career-advice/interviewing/venture-capital-interview-questions?type=Venture_Capital_Resources&title=37%20VC%20Interview%20Questions%20with%20Answers&description=Provides%20a%20set%20of%2037%20venture%20capital%20interview%20questions%20along%20with%20suggested%20answers.",
        "https://www.wallstreetoasis.com/resources/interviews/hedge-funds-interview-questions?type=Hedge_Fund_Resources&title=Hedge%20Fund%20Interview%20Questions&description=A%20collection%20of%20common%20interview%20questions%20faced%20during%20hedge%20fund%20interviews.",
        "https://www.wallstreetprep.com/knowledge/hedge-fund?type=Hedge_Fund_Resources&title=Hedge%20Fund%20Primer&description=An%20introductory%20guide%20to%20understanding%20the%20basic%20concepts%20and%20strategies%20of%20hedge%20funds.",
        "https://mergersandinquisitions.com/how-to-get-a-job-at-a-hedge-fund/?type=Hedge_Fund_Resources&title=How%20to%20Get%20a%20Job%20at%20a%20Hedge%20Fund&description=Detailed%20strategies%20and%20advice%20for%20landing%20a%20job%20in%20the%20hedge%20fund%20industry.",
        "https://www.streetofwalls.com/articles/hedge-fund/?type=Hedge_Fund_Resources&title=Articles%20on%20Hedge%20Funds&description=A%20compilation%20of%20various%20articles%20providing%20in-depth%20insights%20into%20the%20hedge%20fund%20industry.",
        "https://www.wallstreetmojo.com/hedge-fund-interview-questions/?type=Hedge_Fund_Resources&title=Top%2020%20HF%20Interview%20Q%26A&description=Top%2020%20questions%20and%20answers%20to%20expect%20in%20a%20hedge%20fund%20interview.",
        "https://www.daytrading.com/hedge-fund-interview-questions?type=Hedge_Fund_Resources&title=More%20HF%20Interview%20Q%26A&description=Additional%20hedge%20fund%20interview%20questions%20that%20could%20be%20crucial%20for%20candidates.",
        "https://uk.indeed.com/career-advice/interviewing/hedge-fund-interview-questions?type=Hedge_Fund_Resources&title=40%20Hedge%20Fund%20Interview%20Questions%20%28with%20Sample%20Answers%29&description=A%20robust%20list%20of%2040%20hedge%20fund%20interview%20questions%20along%20with%20guidance%20on%20sample%20answers.",
        "https://www.selbyjennings.com/blog/2023/05/preparing-for-a-hedge-fund-interview-your-comprehensive-guide?type=Hedge_Fund_Resources&title=How%20to%20Prepare%20for%20a%20HF%20Interview&description=A%20comprehensive%20guide%20to%20preparing%20for%20hedge%20fund%20interviews%2C%20covering%20what%20to%20know%20and%20how%20to%20present%20oneself.",
        "https://www.efinancialcareers.sg/news/2023/05/hedge-fund-interview-questions?type=Hedge_Fund_Resources&title=Hedge%20Fund%20Interview%20Questions%3A%20What%20to%20Expect%2C%20and%20What%20to%20Ask&description=Insight%20into%20what%20candidates%20can%20expect%20to%20face%20in%20hedge%20fund%20interviews%20and%20suggestions%20on%20what%20questions%20to%20ask.",
        "https://www.buysidehustle.com/most-frequently-asked-hedge-fund-interview-questions-and-answers/?type=Hedge_Fund_Resources&title=Most%20Frequently%20Asked%20HF%20Interview%20Questions&description=Lists%20the%20most%20frequently%20asked%20questions%20in%20hedge%20fund%20interviews%2C%20complete%20with%20answers.",
        "https://www.wallstreetoasis.com/resources/interviews/accounting-interview-questions?type=Accounting_Resources&title=Accounting%20Interview%20Questions&description=A%20list%20of%20common%20questions%20asked%20during%20accounting%20interviews.",
        "https://www.wallstreetprep.com/knowledge/operating-cash-flow-ocf/?type=Accounting_Resources&title=Fundamentals%20of%20Free%20Cash%20Flow%20%28FCF%29&description=Explains%20the%20basics%20of%20calculating%20and%20analyzing%20free%20cash%20flow%2C%20an%20essential%20concept%20in%20accounting%20and%20finance.",
        "https://www.robertwalters.co.uk/insights/career-advice/blog/five-accounting-interview-tips.html?type=Accounting_Resources&title=Tips%20for%20Accounting%20Interview&description=Provides%20practical%20tips%20to%20excel%20in%20accounting%20interviews%2C%20focusing%20on%20how%20to%20present%20technical%20knowledge%20and%20soft%20skills.",
        "https://www.shiksha.com/online-courses/articles/top-accounting-interview-questions-answers/?type=Accounting_Resources&title=Top%20128%20Accounting%20Interview%20Q%26A&description=A%20comprehensive%20list%20of%20accounting%20interview%20questions%20and%20answers%2C%20covering%20a%20wide%20range%20of%20topics%20in%20the%20field.",
        "https://www.franklin.edu/blog/accounting-mvp/accounting-interview-questions?type=Accounting_Resources&title=How%20to%20Prepare%20for%20Accounting%20Interview&description=Discusses%20strategies%20to%20prepare%20for%20an%20accounting%20interview%2C%20including%20understanding%20what%20recruiters%20are%20looking%20for.",
        "https://accountingsoftwareanswers.com/accounting-interview-questions/?type=Accounting_Resources&title=Guide%20for%20an%20Accounting%20Interview&description=A%20guide%20to%20preparing%20for%20accounting%20interviews%2C%20offering%20insights%20into%20the%20types%20of%20questions%20and%20how%20to%20answer%20them%20effectively.",
        "https://www.sienaheights.edu/how-to-prepare-for-accounting-interview-questions/?type=Accounting_Resources&title=How%20to%20Prepare%20for%20Accounting%20Interview%20Questions&description=Provides%20a%20detailed%20approach%20to%20preparing%20for%20accounting%20interviews%2C%20emphasizing%20the%20importance%20of%20practical%20examples%20to%20illustrate%20accounting%20skills.",
        "https://www.remoterocketship.com/advice/6-risk-analyst-interview-questions-with-sample-answers?type=Risk_Analyst_Resources&title=6%20Risk%20Analyst%20Interview%20Questions%20with%20Sample%20Answers&description=This%20page%20provides%20a%20curated%20list%20of%20interview%20questions%20specifically%20for%20risk%20analyst%20positions%20along%20with%20detailed%20sample%20answers%20to%20help%20candidates%20prepare%20effectively.",
        "https://www.investopedia.com/articles/professionals/111115/common-interview-questions-credit-risk-analysts.asp?type=Risk_Analyst_Resources&title=Common%20Interview%20Questions%3A%20Credit%20Risk%20Analysts&description=Investopedia%20outlines%20common%20interview%20questions%20faced%20by%20credit%20risk%20analysts%2C%20offering%20insights%20into%20the%20skills%20and%20knowledge%20expected%20in%20the%20role.",
        "https://www.ziprecruiter.com/career/job-interview-question-answers/risk-analyst?type=Risk_Analyst_Resources&title=Top%2015%20Risk%20Analyst%20Job%20Interview%20Questions%2C%20Answers%20%26%20Tips&description=ZipRecruiter%20presents%20a%20list%20of%20top%20interview%20questions%20for%20risk%20analysts%2C%20including%20tips%20on%20how%20to%20answer%20and%20what%20employers%20are%20looking%20for.",
        "https://www.indeed.com/career-advice/finding-a-job/how-to-become-risk-analyst?type=Risk_Analyst_Resources&title=How%20To%20Become%20a%20Risk%20Analyst%3A%206%20Steps&description=Indeed%20guides%20on%20the%20steps%20to%20becoming%20a%20risk%20analyst%2C%20detailing%20necessary%20education%2C%20skills%2C%20and%20career%20paths.",
        "https://www.theknowledgeacademy.com/blog/risk-management-interview-questions/?type=Risk_Analyst_Resources&title=Top%2040%20Risk%20Management%20Interview%20Questions&description=The%20Knowledge%20Academy%20provides%20a%20comprehensive%20list%20of%20risk%20management%20interview%20questions%20to%20help%20candidates%20prepare%20for%20interviews%20in%20risk%20management%20roles.",
        "https://www.projectpro.io/article/financial-data-scientist/925?type=IT_Resources&title=How%20to%20Become%20a%20Financial%20Data%20Scientist&description=This%20article%20outlines%20the%20initial%20steps%20necessary%20to%20pursue%20a%20career%20as%20a%20financial%20data%20scientist%2C%20emphasizing%20the%20importance%20of%20mastering%20statistical%20concepts%20and%20analytical%20skills.",
        "https://onlinedegrees.sandiego.edu/data-science-in-finance/?type=IT_Resources&title=Data%20Science%20in%20Finance%20%5BCareer%20Guide%5D&description=The%20guide%20explores%20the%20role%20of%20data%20science%20in%20the%20finance%20sector%2C%20detailing%20the%20skills%20required%20and%20the%20impact%20of%20data%20science%20on%20financial%20strategies%20and%20decisions.",
        "https://www.jobzmall.com/careers/financial-data-scientist/faqs/how-can-i-best-prepare-for-a-career-as-a-financial-data-scientist?type=IT_Resources&title=How%20can%20I%20best%20prepare%20for%20a%20career%20as%20a%20Financial%20Data%20Scientist%3F&description=This%20FAQ%20section%20provides%20insights%20into%20the%20preparations%20necessary%20for%20a%20career%20as%20a%20financial%20data%20scientist%2C%20with%20tips%20on%20education%2C%20skills%20development%2C%20and%20practical%20experience."
      ]
    }
  }
}
'''


GPT_TOOL_SCHEMA__BOOK_REFERENCE_small = '''
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "BookRecommendation",
  "type": "object",
  "properties": {
    "recommendation": {
      "type": "string",
      "description": "A recommendation of a book to read with an explanation of why this title was chosen."
    },
    "reference_url": {
      "type": "string",
      "description": "A URL taken from one of the provided references, with the title of the book appended as a query parameter.",
      "enum": [
        "https://www.gutenberg.org/ebooks/2701?title=Moby%20Dick%3B%20Or%2C%20The%20Whale%20by%20Herman%20Melville",
        "https://www.gutenberg.org/ebooks/145?title=Middlemarch%20by%20George%20Eliot",
        "https://www.gutenberg.org/ebooks/2641?title=A%20Room%20with%20a%20View%20by%20E.%20M.%20Forster",
        "https://www.gutenberg.org/ebooks/100?title=The%20Complete%20Works%20of%20William%20Shakespeare%20by%20William%20Shakespeare",
        "https://www.gutenberg.org/ebooks/37106?title=Little%20Women%3B%20Or%2C%20Meg%2C%20Jo%2C%20Beth%2C%20and%20Amy%20by%20Louisa%20May%20Alcott",
        "https://www.gutenberg.org/ebooks/16389?title=The%20Enchanted%20April%20by%20Elizabeth%20Von%20Arnim",
        "https://www.gutenberg.org/ebooks/67979?title=The%20Blue%20Castle%3A%20a%20novel%20by%20L.%20M.%20Montgomery",
        "https://www.gutenberg.org/ebooks/1342?title=Pride%20and%20Prejudice%20by%20Jane%20Austen",
        "https://www.gutenberg.org/ebooks/6761?title=The%20Adventures%20of%20Ferdinand%20Count%20Fathom%20by%20T.%20Smollett",
        "https://www.gutenberg.org/ebooks/394?title=Cranford%20by%20Elizabeth%20Cleghorn%20Gaskell",
        "https://www.gutenberg.org/ebooks/6593?title=History%20of%20Tom%20Jones%2C%20a%20Foundling%20by%20Henry%20Fielding",
        "https://www.gutenberg.org/ebooks/4085?title=The%20Adventures%20of%20Roderick%20Random%20by%20T.%20Smollett",
        "https://www.gutenberg.org/ebooks/2160?title=The%20Expedition%20of%20Humphry%20Clinker%20by%20T.%20Smollett",
        "https://www.gutenberg.org/ebooks/5197?title=My%20Life%20%E2%80%94%20Volume%201%20by%20Richard%20Wagner",
        "https://www.gutenberg.org/ebooks/1259?title=Twenty%20years%20after%20by%20Alexandre%20Dumas%20and%20Auguste%20Maquet",
        "https://www.gutenberg.org/ebooks/4300?title=Ulysses%20by%20James%20Joyce",
        "https://www.gutenberg.org/ebooks/84?title=Frankenstein%3B%20Or%2C%20The%20Modern%20Prometheus%20by%20Mary%20Wollstonecraft%20Shelley",
        "https://www.gutenberg.org/ebooks/11?title=Alice%27s%20Adventures%20in%20Wonderland%20by%20Lewis%20Carroll",
        "https://www.gutenberg.org/ebooks/1080?title=A%20Modest%20Proposal%20by%20Jonathan%20Swift",
        "https://www.gutenberg.org/ebooks/345?title=Dracula%20by%20Bram%20Stoker",
        "https://www.gutenberg.org/ebooks/174?title=The%20Picture%20of%20Dorian%20Gray%20by%20Oscar%20Wilde",
        "https://www.gutenberg.org/ebooks/2554?title=Crime%20and%20Punishment%20by%20Fyodor%20Dostoyevsky",
        "https://www.gutenberg.org/ebooks/2000?title=Don%20Quijote%20by%20Miguel%20de%20Cervantes%20Saavedra",
        "https://www.gutenberg.org/ebooks/5200?title=Metamorphosis%20by%20Franz%20Kafka",
        "https://www.gutenberg.org/ebooks/28054?title=The%20Brothers%20Karamazov%20by%20Fyodor%20Dostoyevsky",
        "https://www.gutenberg.org/ebooks/1661?title=The%20Adventures%20of%20Sherlock%20Holmes%20by%20Arthur%20Conan%20Doyle",
        "https://www.gutenberg.org/ebooks/98?title=A%20Tale%20of%20Two%20Cities%20by%20Charles%20Dickens",
        "https://www.gutenberg.org/ebooks/73838?title=The%20Vatican%20Swindle%20by%20Andr%C3%A9%20Gide",
        "https://www.gutenberg.org/ebooks/64317?title=The%20Great%20Gatsby%20by%20F.%20Scott%20Fitzgerald",
        "https://www.gutenberg.org/ebooks/14859?title=Daddy%20Takes%20Us%20to%20the%20Garden%20by%20Howard%20Roger%20Garis",
        "https://www.gutenberg.org/ebooks/996?title=Don%20Quixote%20by%20Miguel%20de%20Cervantes%20Saavedra",
        "https://www.gutenberg.org/ebooks/76?title=Adventures%20of%20Huckleberry%20Finn%20by%20Mark%20Twain",
        "https://www.gutenberg.org/ebooks/1998?title=Thus%20Spake%20Zarathustra%3A%20A%20Book%20for%20All%20and%20None%20by%20Friedrich%20Wilhelm%20Nietzsche",
        "https://www.gutenberg.org/ebooks/6130?title=The%20Iliad%20by%20Homer",
        "https://www.gutenberg.org/ebooks/30254?title=The%20Romance%20of%20Lust%3A%20A%20classic%20Victorian%20erotic%20novel%20by%20Anonymous",
        "https://www.gutenberg.org/ebooks/1400?title=Great%20Expectations%20by%20Charles%20Dickens",
        "https://www.gutenberg.org/ebooks/2542?title=A%20Doll%27s%20House%3A%20A%20play%20by%20Henrik%20Ibsen",
        "https://www.gutenberg.org/ebooks/27827?title=The%20Kama%20Sutra%20of%20Vatsyayana%20by%20Vatsyayana",
        "https://www.gutenberg.org/ebooks/2600?title=War%20and%20Peace%20by%20graf%20Leo%20Tolstoy",
        "https://www.gutenberg.org/ebooks/2591?title=Grimms%27%20Fairy%20Tales%20by%20Jacob%20Grimm%20and%20Wilhelm%20Grimm",
        "https://www.gutenberg.org/ebooks/1260?title=Jane%20Eyre%3A%20An%20Autobiography%20by%20Charlotte%20Bront%C3%AB",
        "https://www.gutenberg.org/ebooks/1952?title=The%20Yellow%20Wallpaper%20by%20Charlotte%20Perkins%20Gilman",
        "https://www.gutenberg.org/ebooks/600?title=Notes%20from%20the%20Underground%20by%20Fyodor%20Dostoyevsky",
        "https://www.gutenberg.org/ebooks/398?title=The%20First%20Book%20of%20Adam%20and%20Eve%20by%20Rutherford%20Hayes%20Platt",
        "https://www.gutenberg.org/ebooks/20738?title=Diccionario%20Ingles-Espa%C3%B1ol-Tagalog%20by%20Sofronio%20G.%20Calder%C3%B3n",
        "https://www.gutenberg.org/ebooks/73828?title=From%20the%20Arctic%20Ocean%20to%20the%20Yellow%20Sea%20by%20Julius%20M.%20Price",
        "https://www.gutenberg.org/ebooks/1?title=The%20Declaration%20of%20Independence%20of%20the%20United%20States%20of%20America%20by%20Thomas%20Jefferson",
        "https://www.gutenberg.org/ebooks/730?title=Oliver%20Twist%20by%20Charles%20Dickens",
        "https://www.gutenberg.org/ebooks/17489?title=Les%20miserables%20Tome%20I%3A%20Fantine%20by%20Victor%20Hugo",
        "https://www.gutenberg.org/ebooks/41?title=The%20Legend%20of%20Sleepy%20Hollow%20by%20Washington%20Irving",
        "https://www.gutenberg.org/ebooks/3207?title=Leviathan%20by%20Thomas%20Hobbes",
        "https://www.gutenberg.org/ebooks/25344?title=The%20Scarlet%20Letter%20by%20Nathaniel%20Hawthorne",
        "https://www.gutenberg.org/ebooks/4217?title=A%20Portrait%20of%20the%20Artist%20as%20a%20Young%20Man%20by%20James%20Joyce",
        "https://www.gutenberg.org/ebooks/26839?title=Mathematical%20Recreations%20and%20Essays%20by%20W.%20W.%20Rouse%20Ball",
        "https://www.gutenberg.org/ebooks/12?title=Through%20the%20Looking-Glass%20by%20Lewis%20Carroll",
        "https://www.gutenberg.org/ebooks/5827?title=The%20Problems%20of%20Philosophy%20by%20Bertrand%20Russell",
        "https://www.gutenberg.org/ebooks/19616?title=Aesop%27s%20Fables%20-%20Volume%2001%20by%20Aesop",
        "https://www.gutenberg.org/ebooks/58221?title=La%20Odisea%20by%20Homer"
      ]
    }
  },
  "required": ["recommendation", "reference_url"],
  "additionalProperties": false
}

'''

GPT_TOOL_SCHEMA__BOOK_REFERENCE_work = """
{
    type: object,
    properties: {
      recommendation: {
        type: string,
        description: A recommendation of a book to read with an explanation of why this title was chosen.
      },
      reference_url: {
        type: string,
        description: A URL and title taken from one of the provided references separated by |||,
        enum: [
            https_//www.gutenberg.org/ebooks/2701|||Moby Dick; Or The Whale by Herman Melville,
            https_//www.gutenberg.org/ebooks/145|||Middlemarch by George Eliot,
            https_//www.gutenberg.org/ebooks/2641|||A Room with a View by E. M. Forster,
            https_//www.gutenberg.org/ebooks/100|||The Complete Works of William Shakespeare by William Shakespeare,
            https_//www.gutenberg.org/ebooks/37106|||Little Women; Or Meg Jo Beth and Amy by Louisa May Alcott,
            https_//www.gutenberg.org/ebooks/16389|||The Enchanted April by Elizabeth Von Arnim,
            https_//www.gutenberg.org/ebooks/67979|||The Blue Castle a novel by L. M. Montgomery,
            https_//www.gutenberg.org/ebooks/1342|||Pride and Prejudice by Jane Austen,
            https_//www.gutenberg.org/ebooks/6761|||The Adventures of Ferdinand Count Fathom by T. Smollett,
            https_//www.gutenberg.org/ebooks/394|||Cranford by Elizabeth Cleghorn Gaskell,
            https_//www.gutenberg.org/ebooks/6593|||History of Tom Jones a Foundling by Henry Fielding,
            https_//www.gutenberg.org/ebooks/4085|||The Adventures of Roderick Random by T. Smollett,
            https_//www.gutenberg.org/ebooks/2160|||The Expedition of Humphry Clinker by T. Smollett,
            https_//www.gutenberg.org/ebooks/5197|||My Life — Volume 1 by Richard Wagner,
            https_//www.gutenberg.org/ebooks/1259|||Twenty years after by Alexandre Dumas and Auguste Maquet,
            https_//www.gutenberg.org/ebooks/4300|||Ulysses by James Joyce,
            https_//www.gutenberg.org/ebooks/84|||Frankenstein; Or The Modern Prometheus by Mary Wollstonecraft Shelley,
            https_//www.gutenberg.org/ebooks/11|||Alice's Adventures in Wonderland by Lewis Carroll,
            https_//www.gutenberg.org/ebooks/1080|||A Modest Proposal by Jonathan Swift,
            https_//www.gutenberg.org/ebooks/345|||Dracula by Bram Stoker,
            https_//www.gutenberg.org/ebooks/174|||The Picture of Dorian Gray by Oscar Wilde,
            https_//www.gutenberg.org/ebooks/2554|||Crime and Punishment by Fyodor Dostoyevsky,
            https_//www.gutenberg.org/ebooks/2000|||Don Quijote by Miguel de Cervantes Saavedra,
            https_//www.gutenberg.org/ebooks/5200|||Metamorphosis by Franz Kafka,
            https_//www.gutenberg.org/ebooks/28054|||The Brothers Karamazov by Fyodor Dostoyevsky,
            https_//www.gutenberg.org/ebooks/1661|||The Adventures of Sherlock Holmes by Arthur Conan Doyle,
            https_//www.gutenberg.org/ebooks/98|||A Tale of Two Cities by Charles Dickens,
            https_//www.gutenberg.org/ebooks/73838|||The Vatican Swindle by André Gide,
            https_//www.gutenberg.org/ebooks/64317|||The Great Gatsby by F. Scott Fitzgerald,
            https_//www.gutenberg.org/ebooks/14859|||Daddy Takes Us to the Garden by Howard Roger Garis,
            https_//www.gutenberg.org/ebooks/996|||Don Quixote by Miguel de Cervantes Saavedra,
            https_//www.gutenberg.org/ebooks/76|||Adventures of Huckleberry Finn by Mark Twain,
            https_//www.gutenberg.org/ebooks/1998|||Thus Spake Zarathustra - A Book for All and None by Friedrich Wilhelm Nietzsche,
            https_//www.gutenberg.org/ebooks/6130|||The Iliad by Homer,
            https_//www.gutenberg.org/ebooks/30254|||The Romance of Lust - A classic Victorian erotic novel by Anonymous,
            https_//www.gutenberg.org/ebooks/1400|||Great Expectations by Charles Dickens,
            https_//www.gutenberg.org/ebooks/2542|||A Doll's House - A play by Henrik Ibsen,
            https_//www.gutenberg.org/ebooks/27827|||The Kama Sutra of Vatsyayana by Vatsyayana,
            https_//www.gutenberg.org/ebooks/2600|||War and Peace by graf Leo Tolstoy,
            https_//www.gutenberg.org/ebooks/2591|||Grimms' Fairy Tales by Jacob Grimm and Wilhelm Grimm,
            https_//www.gutenberg.org/ebooks/1260|||Jane Eyre - An Autobiography by Charlotte Brontë,
            https_//www.gutenberg.org/ebooks/1952|||The Yellow Wallpaper by Charlotte Perkins Gilman,
            https_//www.gutenberg.org/ebooks/5740|||Tractatus Logico-Philosophicus by Ludwig Wittgenstein,
            https_//www.gutenberg.org/ebooks/844|||The Importance of Being Earnest - A Trivial Comedy for Serious People by Oscar Wilde,
            https_//www.gutenberg.org/ebooks/1184|||The Count of Monte Cristo by Alexandre Dumas and Auguste Maquet,
            https_//www.gutenberg.org/ebooks/43|||The Strange Case of Dr. Jekyll and Mr. Hyde by Robert Louis Stevenson,
            https_//www.gutenberg.org/ebooks/31552|||Novo dicionário da língua portuguesa by Cândido de Figueiredo,
            https_//www.gutenberg.org/ebooks/244|||A Study in Scarlet by Arthur Conan Doyle,
            https_//www.gutenberg.org/ebooks/16119|||Doctrina Christiana,
            https_//www.gutenberg.org/ebooks/46|||A Christmas Carol in Prose; Being a Ghost Story of Christmas by Charles Dickens,
            https_//www.gutenberg.org/ebooks/1232|||The Prince by Niccolò Machiavelli,
            https_//www.gutenberg.org/ebooks/74|||The Adventures of Tom Sawyer by Mark Twain,
            https_//www.gutenberg.org/ebooks/2446|||An Enemy of the People by Henrik Ibsen,
            https_//www.gutenberg.org/ebooks/45|||Anne of Green Gables by L. M. Montgomery,
            https_//www.gutenberg.org/ebooks/219|||Heart of Darkness by Joseph Conrad,
            https_//www.gutenberg.org/ebooks/2814|||Dubliners by James Joyce,
            https_//www.gutenberg.org/ebooks/10|||The King James Version of the Bible,
            https_//www.gutenberg.org/ebooks/2650|||Du côté de chez Swann by Marcel Proust,
            https_//www.gutenberg.org/ebooks/73834|||A First Book in Organic Evolution by D. Kerfoot Shute,
            https_//www.gutenberg.org/ebooks/16|||Peter Pan by J. M. Barrie,
            https_//www.gutenberg.org/ebooks/2680|||Meditations by Emperor of Rome Marcus Aurelius,
            https_//www.gutenberg.org/ebooks/8492|||The King in Yellow by Robert W. Chambers,
            https_//www.gutenberg.org/ebooks/1727|||The Odyssey by Homer,
            https_//www.gutenberg.org/ebooks/67098|||Winnie-the-Pooh by A. A. Milne,
            https_//www.gutenberg.org/ebooks/33283|||Calculus Made Easy by Silvanus P. Thompson,
            https_//www.gutenberg.org/ebooks/768|||Wuthering Heights by Emily Brontë,
            https_//www.gutenberg.org/ebooks/205|||Walden and On The Duty Of Civil Disobedience by Henry David Thoreau,
            https_//www.gutenberg.org/ebooks/58585|||The Prophet by Kahlil Gibran,
            https_//www.gutenberg.org/ebooks/22091|||The Best Short Stories of 1920 and the Yearbook of the American Short Story,
            https_//www.gutenberg.org/ebooks/4363|||Beyond Good and Evil by Friedrich Wilhelm Nietzsche,
            https_//www.gutenberg.org/ebooks/1497|||The Republic by Plato,
            https_//www.gutenberg.org/ebooks/27509|||The 2006 CIA World Factbook by United States. Central Intelligence Agency,
            https_//www.gutenberg.org/ebooks/31284|||Josefine Mutzenbacher by Felix Salten,
            https_//www.gutenberg.org/ebooks/158|||Emma by Jane Austen,
            https_//www.gutenberg.org/ebooks/36034|||White Nights and Other Stories by Fyodor Dostoyevsky,
            https_//www.gutenberg.org/ebooks/135|||Les Misérables by Victor Hugo,
            https_//www.gutenberg.org/ebooks/1946|||On War by Carl von Clausewitz,
            https_//www.gutenberg.org/ebooks/36|||The War of the Worlds by H. G. Wells,
            https_//www.gutenberg.org/ebooks/1399|||Anna Karenina by graf Leo Tolstoy,
            https_//www.gutenberg.org/ebooks/120|||Treasure Island by Robert Louis Stevenson,
            https_//www.gutenberg.org/ebooks/8800|||The Divine Comedy by Dante Alighieri,
            https_//www.gutenberg.org/ebooks/55|||The Wonderful Wizard of Oz by L. Frank Baum,
            https_//www.gutenberg.org/ebooks/514|||Little Women by Louisa May Alcott,
            https_//www.gutenberg.org/ebooks/600|||Notes from the Underground by Fyodor Dostoyevsky,
            https_//www.gutenberg.org/ebooks/398|||The First Book of Adam and Eve by Rutherford Hayes Platt,
            https_//www.gutenberg.org/ebooks/20738|||Diccionario Ingles-Español-Tagalog by Sofronio G. Calderón,
            https_//www.gutenberg.org/ebooks/73828|||From the Arctic Ocean to the Yellow Sea by Julius M. Price,
            https_//www.gutenberg.org/ebooks/1|||The Declaration of Independence of the United States of America by Thomas Jefferson,
            https_//www.gutenberg.org/ebooks/730|||Oliver Twist by Charles Dickens,
            https_//www.gutenberg.org/ebooks/17489|||Les misérables Tome I - Fantine by Victor Hugo,
            https_//www.gutenberg.org/ebooks/41|||The Legend of Sleepy Hollow by Washington Irving,
            https_//www.gutenberg.org/ebooks/3207|||Leviathan by Thomas Hobbes,
            https_//www.gutenberg.org/ebooks/25344|||The Scarlet Letter by Nathaniel Hawthorne,
            https_//www.gutenberg.org/ebooks/4217|||A Portrait of the Artist as a Young Man by James Joyce,
            https_//www.gutenberg.org/ebooks/26839|||Mathematical Recreations and Essays by W. W. Rouse Ball,
            https_//www.gutenberg.org/ebooks/12|||Through the Looking-Glass by Lewis Carroll,
            https_//www.gutenberg.org/ebooks/5827|||The Problems of Philosophy by Bertrand Russell,
            https_//www.gutenberg.org/ebooks/19616|||Aesop's Fables - Volume 01 by Aesop,
            https_//www.gutenberg.org/ebooks/58221|||La Odisea by Homer
        ]
      }
    },
    required: [
      recommendation,
      reference_url
    ]
}
"""

GPT_TOOL_SCHEMA__BOOK_REFERENCE = """
{
  type: function,
  function: {
      name: book_recommendation,
      description: Generate a book recommendation with reference,
      parameters: {
          type: object,
          properties: {
              recommendation: {
                  type: string,
                  description: A recommendation of a book to read with an explanation of why this title was chosen.,
              },
              reference_url: {
                  type: string,
                  description: A URL and title taken from one of the provided references separated by |||.,
                  enum: [
                      https://www.gutenberg.org/ebooks/2701|||Moby Dick; Or The Whale by Herman Melville,
                      https://www.gutenberg.org/ebooks/145|||Middlemarch by George Eliot,
                      https://www.gutenberg.org/ebooks/2641|||A Room with a View by E. M. Forster,
                      https://www.gutenberg.org/ebooks/100|||The Complete Works of William Shakespeare by William Shakespeare,
                      https://www.gutenberg.org/ebooks/37106|||Little Women; Or Meg Jo Beth and Amy by Louisa May Alcott,
                      https://www.gutenberg.org/ebooks/16389|||The Enchanted April by Elizabeth Von Arnim,
                      https://www.gutenberg.org/ebooks/67979|||The Blue Castle: a novel by L. M. Montgomery,
                      https://www.gutenberg.org/ebooks/1342|||Pride and Prejudice by Jane Austen,
                      https://www.gutenberg.org/ebooks/6761|||The Adventures of Ferdinand Count Fathom by T. Smollett,
                      https://www.gutenberg.org/ebooks/394|||Cranford by Elizabeth Cleghorn Gaskell,
                      https://www.gutenberg.org/ebooks/6593|||History of Tom Jones a Foundling by Henry Fielding,
                      https://www.gutenberg.org/ebooks/4085|||The Adventures of Roderick Random by T. Smollett,
                      https://www.gutenberg.org/ebooks/2160|||The Expedition of Humphry Clinker by T. Smollett,
                      https://www.gutenberg.org/ebooks/5197|||My Life — Volume 1 by Richard Wagner,
                      https://www.gutenberg.org/ebooks/1259|||Twenty years after by Alexandre Dumas and Auguste Maquet,
                      https://www.gutenberg.org/ebooks/4300|||Ulysses by James Joyce,
                      https://www.gutenberg.org/ebooks/84|||Frankenstein; Or The Modern Prometheus by Mary Wollstonecraft Shelley,
                      https://www.gutenberg.org/ebooks/11|||Alice's Adventures in Wonderland by Lewis Carroll,
                      https://www.gutenberg.org/ebooks/1080|||A Modest Proposal by Jonathan Swift,
                      https://www.gutenberg.org/ebooks/345|||Dracula by Bram Stoker,
                      https://www.gutenberg.org/ebooks/174|||The Picture of Dorian Gray by Oscar Wilde,
                      https://www.gutenberg.org/ebooks/2554|||Crime and Punishment by Fyodor Dostoyevsky,
                      https://www.gutenberg.org/ebooks/2000|||Don Quijote by Miguel de Cervantes Saavedra,
                      https://www.gutenberg.org/ebooks/5200|||Metamorphosis by Franz Kafka,
                      https://www.gutenberg.org/ebooks/28054|||The Brothers Karamazov by Fyodor Dostoyevsky,
                      https://www.gutenberg.org/ebooks/1661|||The Adventures of Sherlock Holmes by Arthur Conan Doyle,
                      https://www.gutenberg.org/ebooks/98|||A Tale of Two Cities by Charles Dickens,
                      https://www.gutenberg.org/ebooks/73838|||The Vatican Swindle by André Gide,
                      https://www.gutenberg.org/ebooks/64317|||The Great Gatsby by F. Scott Fitzgerald,
                      https://www.gutenberg.org/ebooks/14859|||Daddy Takes Us to the Garden by Howard Roger Garis,
                      https://www.gutenberg.org/ebooks/996|||Don Quixote by Miguel de Cervantes Saavedra,
                      https://www.gutenberg.org/ebooks/76|||Adventures of Huckleberry Finn by Mark Twain,
                      https://www.gutenberg.org/ebooks/1998|||Thus Spake Zarathustra: A Book for All and None by Friedrich Wilhelm Nietzsche,
                      https://www.gutenberg.org/ebooks/6130|||The Iliad by Homer,
                      https://www.gutenberg.org/ebooks/30254|||The Romance of Lust: A classic Victorian erotic novel by Anonymous,
                      https://www.gutenberg.org/ebooks/1400|||Great Expectations by Charles Dickens,
                      https://www.gutenberg.org/ebooks/2542|||A Doll's House: A play by Henrik Ibsen,
                      https://www.gutenberg.org/ebooks/27827|||The Kama Sutra of Vatsyayana by Vatsyayana,
                      https://www.gutenberg.org/ebooks/2600|||War and Peace by graf Leo Tolstoy,
                      https://www.gutenberg.org/ebooks/2591|||Grimms' Fairy Tales by Jacob Grimm and Wilhelm Grimm,
                      https://www.gutenberg.org/ebooks/1260|||Jane Eyre: An Autobiography by Charlotte Brontë,
                      https://www.gutenberg.org/ebooks/1952|||The Yellow Wallpaper by Charlotte Perkins Gilman,
                      https://www.gutenberg.org/ebooks/5740|||Tractatus Logico-Philosophicus by Ludwig Wittgenstein,
                      https://www.gutenberg.org/ebooks/844|||The Importance of Being Earnest: A Trivial Comedy for Serious People by Oscar Wilde,
                      https://www.gutenberg.org/ebooks/1184|||The Count of Monte Cristo by Alexandre Dumas and Auguste Maquet,
                      https://www.gutenberg.org/ebooks/43|||The Strange Case of Dr. Jekyll and Mr. Hyde by Robert Louis Stevenson,
                      https://www.gutenberg.org/ebooks/31552|||Novo dicionário da língua portuguesa by Cândido de Figueiredo,
                      https://www.gutenberg.org/ebooks/244|||A Study in Scarlet by Arthur Conan Doyle,
                      https://www.gutenberg.org/ebooks/16119|||Doctrina Christiana,
                      https://www.gutenberg.org/ebooks/46|||A Christmas Carol in Prose; Being a Ghost Story of Christmas by Charles Dickens,
                      https://www.gutenberg.org/ebooks/1232|||The Prince by Niccolò Machiavelli,
                      https://www.gutenberg.org/ebooks/74|||The Adventures of Tom Sawyer by Mark Twain,
                      https://www.gutenberg.org/ebooks/2446|||An Enemy of the People by Henrik Ibsen,
                      https://www.gutenberg.org/ebooks/45|||Anne of Green Gables by L. M. Montgomery,
                      https://www.gutenberg.org/ebooks/219|||Heart of Darkness by Joseph Conrad,
                      https://www.gutenberg.org/ebooks/2814|||Dubliners by James Joyce,
                      https://www.gutenberg.org/ebooks/10|||The King James Version of the Bible,
                      https://www.gutenberg.org/ebooks/2650|||Du côté de chez Swann by Marcel Proust,
                      https://www.gutenberg.org/ebooks/73834|||A First Book in Organic Evolution by D. Kerfoot Shute,
                      https://www.gutenberg.org/ebooks/16|||Peter Pan by J. M. Barrie,
                      https://www.gutenberg.org/ebooks/2680|||Meditations by Emperor of Rome Marcus Aurelius,
                      https://www.gutenberg.org/ebooks/8492|||The King in Yellow by Robert W. Chambers,
                      https://www.gutenberg.org/ebooks/1727|||The Odyssey by Homer,
                      https://www.gutenberg.org/ebooks/67098|||Winnie-the-Pooh by A. A. Milne,
                      https://www.gutenberg.org/ebooks/33283|||Calculus Made Easy by Silvanus P. Thompson,
                      https://www.gutenberg.org/ebooks/768|||Wuthering Heights by Emily Brontë,
                      https://www.gutenberg.org/ebooks/205|||Walden and On The Duty Of Civil Disobedience by Henry David Thoreau,
                      https://www.gutenberg.org/ebooks/58585|||The Prophet by Kahlil Gibran,
                      https://www.gutenberg.org/ebooks/22091|||The Best Short Stories of 1920, and the Yearbook of the American Short Story,
                      https://www.gutenberg.org/ebooks/4363|||Beyond Good and Evil by Friedrich Wilhelm Nietzsche,
                      https://www.gutenberg.org/ebooks/1497|||The Republic by Plato,
                      https://www.gutenberg.org/ebooks/27509|||The 2006 CIA World Factbook by United States. Central Intelligence Agency,
                      https://www.gutenberg.org/ebooks/31284|||Josefine Mutzenbacher by Felix Salten,
                      https://www.gutenberg.org/ebooks/158|||Emma by Jane Austen,
                      https://www.gutenberg.org/ebooks/36034|||White Nights and Other Stories by Fyodor Dostoyevsky,
                      https://www.gutenberg.org/ebooks/135|||Les Misérables by Victor Hugo,
                      https://www.gutenberg.org/ebooks/1946|||On War by Carl von Clausewitz,
                      https://www.gutenberg.org/ebooks/36|||The War of the Worlds by H. G. Wells,
                      https://www.gutenberg.org/ebooks/1399|||Anna Karenina by graf Leo Tolstoy,
                      https://www.gutenberg.org/ebooks/120|||Treasure Island by Robert Louis Stevenson,
                      https://www.gutenberg.org/ebooks/8800|||The Divine Comedy by Dante Alighieri,
                      https://www.gutenberg.org/ebooks/55|||The Wonderful Wizard of Oz by L. Frank Baum,
                      https://www.gutenberg.org/ebooks/514|||Little Women by Louisa May Alcott,
                      https://www.gutenberg.org/ebooks/600|||Notes from the Underground by Fyodor Dostoyevsky,
                      https://www.gutenberg.org/ebooks/398|||The First Book of Adam and Eve by Rutherford Hayes Platt,
                      https://www.gutenberg.org/ebooks/20738|||Diccionario Ingles-Español-Tagalog by Sofronio G. Calderón,
                      https://www.gutenberg.org/ebooks/73828|||From the Arctic Ocean to the Yellow Sea by Julius M. Price,
                      https://www.gutenberg.org/ebooks/1|||The Declaration of Independence of the United States of America by Thomas Jefferson,
                      https://www.gutenberg.org/ebooks/730|||Oliver Twist by Charles Dickens,
                      https://www.gutenberg.org/ebooks/17489|||Les misérables Tome I: Fantine by Victor Hugo,
                      https://www.gutenberg.org/ebooks/41|||The Legend of Sleepy Hollow by Washington Irving,
                      https://www.gutenberg.org/ebooks/3207|||Leviathan by Thomas Hobbes,
                      https://www.gutenberg.org/ebooks/25344|||The Scarlet Letter by Nathaniel Hawthorne,
                      https://www.gutenberg.org/ebooks/4217|||A Portrait of the Artist as a Young Man by James Joyce,
                      https://www.gutenberg.org/ebooks/26839|||Mathematical Recreations and Essays by W. W. Rouse Ball,
                      https://www.gutenberg.org/ebooks/12|||Through the Looking-Glass by Lewis Carroll,
                      https://www.gutenberg.org/ebooks/5827|||The Problems of Philosophy by Bertrand Russell,
                      https://www.gutenberg.org/ebooks/19616|||Aesop's Fables - Volume 01 by Aesop,
                      https://www.gutenberg.org/ebooks/58221|||La Odisea by Homer,
                  ],
              },
          },
          required: [recommendation, reference_url]
      },
"""

GPT_TOOL_REF_SCHEMA_FULL = {
    "type": "function",
    "function": {
        "name": "book_recommendation",
        "description": "Generate a book recommendation with reference",
        "parameters": {
            "type": "object",
            "properties": {
                "recommendation": {
                    "type": "string",
                    "description": "A recommendation of a book to read with an explanation of why this title was chosen.",
                },
                "reference_url": {
                    "type": "string",
                    "description": "A URL and title taken from one of the provided references, separated by '|||'.",
                    "enum": [
                        "https://www.gutenberg.org/ebooks/2701|||Moby Dick; Or, The Whale by Herman Melville",
                        "https://www.gutenberg.org/ebooks/145|||Middlemarch by George Eliot",
                        "https://www.gutenberg.org/ebooks/2641|||A Room with a View by E. M. Forster",
                        "https://www.gutenberg.org/ebooks/100|||The Complete Works of William Shakespeare by William Shakespeare",
                        "https://www.gutenberg.org/ebooks/37106|||Little Women; Or, Meg, Jo, Beth, and Amy by Louisa May Alcott",
                        "https://www.gutenberg.org/ebooks/16389|||The Enchanted April by Elizabeth Von Arnim",
                        "https://www.gutenberg.org/ebooks/67979|||The Blue Castle: a novel by L. M. Montgomery",
                        "https://www.gutenberg.org/ebooks/1342|||Pride and Prejudice by Jane Austen",
                        "https://www.gutenberg.org/ebooks/6761|||The Adventures of Ferdinand Count Fathom by T. Smollett",
                        "https://www.gutenberg.org/ebooks/394|||Cranford by Elizabeth Cleghorn Gaskell",
                        "https://www.gutenberg.org/ebooks/6593|||History of Tom Jones, a Foundling by Henry Fielding",
                        "https://www.gutenberg.org/ebooks/4085|||The Adventures of Roderick Random by T. Smollett",
                        "https://www.gutenberg.org/ebooks/2160|||The Expedition of Humphry Clinker by T. Smollett",
                        "https://www.gutenberg.org/ebooks/5197|||My Life — Volume 1 by Richard Wagner",
                        "https://www.gutenberg.org/ebooks/1259|||Twenty years after by Alexandre Dumas and Auguste Maquet",
                        "https://www.gutenberg.org/ebooks/4300|||Ulysses by James Joyce",
                        "https://www.gutenberg.org/ebooks/84|||Frankenstein; Or, The Modern Prometheus by Mary Wollstonecraft Shelley",
                        "https://www.gutenberg.org/ebooks/11|||Alice's Adventures in Wonderland by Lewis Carroll",
                        "https://www.gutenberg.org/ebooks/1080|||A Modest Proposal by Jonathan Swift",
                        "https://www.gutenberg.org/ebooks/345|||Dracula by Bram Stoker",
                        "https://www.gutenberg.org/ebooks/174|||The Picture of Dorian Gray by Oscar Wilde",
                        "https://www.gutenberg.org/ebooks/2554|||Crime and Punishment by Fyodor Dostoyevsky",
                        "https://www.gutenberg.org/ebooks/2000|||Don Quijote by Miguel de Cervantes Saavedra",
                        "https://www.gutenberg.org/ebooks/5200|||Metamorphosis by Franz Kafka",
                        "https://www.gutenberg.org/ebooks/28054|||The Brothers Karamazov by Fyodor Dostoyevsky",
                        "https://www.gutenberg.org/ebooks/1661|||The Adventures of Sherlock Holmes by Arthur Conan Doyle",
                        "https://www.gutenberg.org/ebooks/98|||A Tale of Two Cities by Charles Dickens",
                        "https://www.gutenberg.org/ebooks/73838|||The Vatican Swindle by André Gide",
                        "https://www.gutenberg.org/ebooks/64317|||The Great Gatsby by F. Scott Fitzgerald",
                        "https://www.gutenberg.org/ebooks/14859|||Daddy Takes Us to the Garden by Howard Roger Garis",
                        "https://www.gutenberg.org/ebooks/996|||Don Quixote by Miguel de Cervantes Saavedra",
                        "https://www.gutenberg.org/ebooks/76|||Adventures of Huckleberry Finn by Mark Twain",
                        "https://www.gutenberg.org/ebooks/1998|||Thus Spake Zarathustra: A Book for All and None by Friedrich Wilhelm Nietzsche",
                        "https://www.gutenberg.org/ebooks/6130|||The Iliad by Homer",
                        "https://www.gutenberg.org/ebooks/30254|||The Romance of Lust: A classic Victorian erotic novel by Anonymous",
                        "https://www.gutenberg.org/ebooks/1400|||Great Expectations by Charles Dickens",
                        "https://www.gutenberg.org/ebooks/2542|||A Doll's House: A play by Henrik Ibsen",
                        "https://www.gutenberg.org/ebooks/27827|||The Kama Sutra of Vatsyayana by Vatsyayana",
                        "https://www.gutenberg.org/ebooks/2600|||War and Peace by graf Leo Tolstoy",
                        "https://www.gutenberg.org/ebooks/2591|||Grimms' Fairy Tales by Jacob Grimm and Wilhelm Grimm",
                        "https://www.gutenberg.org/ebooks/1260|||Jane Eyre: An Autobiography by Charlotte Brontë",
                        "https://www.gutenberg.org/ebooks/1952|||The Yellow Wallpaper by Charlotte Perkins Gilman",
                        "https://www.gutenberg.org/ebooks/5740|||Tractatus Logico-Philosophicus by Ludwig Wittgenstein",
                        "https://www.gutenberg.org/ebooks/844|||The Importance of Being Earnest: A Trivial Comedy for Serious People by Oscar Wilde",
                        "https://www.gutenberg.org/ebooks/1184|||The Count of Monte Cristo by Alexandre Dumas and Auguste Maquet",
                        "https://www.gutenberg.org/ebooks/43|||The Strange Case of Dr. Jekyll and Mr. Hyde by Robert Louis Stevenson",
                        "https://www.gutenberg.org/ebooks/31552|||Novo dicionário da língua portuguesa by Cândido de Figueiredo",
                        "https://www.gutenberg.org/ebooks/244|||A Study in Scarlet by Arthur Conan Doyle",
                        "https://www.gutenberg.org/ebooks/16119|||Doctrina Christiana",
                        "https://www.gutenberg.org/ebooks/46|||A Christmas Carol in Prose; Being a Ghost Story of Christmas by Charles Dickens",
                        "https://www.gutenberg.org/ebooks/1232|||The Prince by Niccolò Machiavelli",
                        "https://www.gutenberg.org/ebooks/74|||The Adventures of Tom Sawyer by Mark Twain",
                        "https://www.gutenberg.org/ebooks/2446|||An Enemy of the People by Henrik Ibsen",
                        "https://www.gutenberg.org/ebooks/45|||Anne of Green Gables by L. M. Montgomery",
                        "https://www.gutenberg.org/ebooks/219|||Heart of Darkness by Joseph Conrad",
                        "https://www.gutenberg.org/ebooks/2814|||Dubliners by James Joyce",
                        "https://www.gutenberg.org/ebooks/10|||The King James Version of the Bible",
                        "https://www.gutenberg.org/ebooks/2650|||Du côté de chez Swann by Marcel Proust",
                        "https://www.gutenberg.org/ebooks/73834|||A First Book in Organic Evolution by D. Kerfoot Shute",
                        "https://www.gutenberg.org/ebooks/16|||Peter Pan by J. M. Barrie",
                        "https://www.gutenberg.org/ebooks/2680|||Meditations by Emperor of Rome Marcus Aurelius",
                        "https://www.gutenberg.org/ebooks/8492|||The King in Yellow by Robert W. Chambers",
                        "https://www.gutenberg.org/ebooks/1727|||The Odyssey by Homer",
                        "https://www.gutenberg.org/ebooks/67098|||Winnie-the-Pooh by A. A. Milne",
                        "https://www.gutenberg.org/ebooks/33283|||Calculus Made Easy by Silvanus P. Thompson",
                        "https://www.gutenberg.org/ebooks/768|||Wuthering Heights by Emily Brontë",
                        "https://www.gutenberg.org/ebooks/205|||Walden, and On The Duty Of Civil Disobedience by Henry David Thoreau",
                        "https://www.gutenberg.org/ebooks/58585|||The Prophet by Kahlil Gibran",
                        "https://www.gutenberg.org/ebooks/22091|||The Best Short Stories of 1920, and the Yearbook of the American Short Story",
                        "https://www.gutenberg.org/ebooks/4363|||Beyond Good and Evil by Friedrich Wilhelm Nietzsche",
                        "https://www.gutenberg.org/ebooks/1497|||The Republic by Plato",
                        "https://www.gutenberg.org/ebooks/27509|||The 2006 CIA World Factbook by United States. Central Intelligence Agency",
                        "https://www.gutenberg.org/ebooks/31284|||Josefine Mutzenbacher by Felix Salten",
                        "https://www.gutenberg.org/ebooks/158|||Emma by Jane Austen",
                        "https://www.gutenberg.org/ebooks/36034|||White Nights and Other Stories by Fyodor Dostoyevsky",
                        "https://www.gutenberg.org/ebooks/135|||Les Misérables by Victor Hugo",
                        "https://www.gutenberg.org/ebooks/1946|||On War by Carl von Clausewitz",
                        "https://www.gutenberg.org/ebooks/36|||The War of the Worlds by H. G. Wells",
                        "https://www.gutenberg.org/ebooks/1399|||Anna Karenina by graf Leo Tolstoy",
                        "https://www.gutenberg.org/ebooks/120|||Treasure Island by Robert Louis Stevenson",
                        "https://www.gutenberg.org/ebooks/8800|||The Divine Comedy by Dante Alighieri",
                        "https://www.gutenberg.org/ebooks/55|||The Wonderful Wizard of Oz by L. Frank Baum",
                        "https://www.gutenberg.org/ebooks/514|||Little Women by Louisa May Alcott",
                        "https://www.gutenberg.org/ebooks/600|||Notes from the Underground by Fyodor Dostoyevsky",
                        "https://www.gutenberg.org/ebooks/398|||The First Book of Adam and Eve by Rutherford Hayes Platt",
                        "https://www.gutenberg.org/ebooks/20738|||Diccionario Ingles-Español-Tagalog by Sofronio G. Calderón",
                        "https://www.gutenberg.org/ebooks/73828|||From the Arctic Ocean to the Yellow Sea by Julius M. Price",
                        "https://www.gutenberg.org/ebooks/1|||The Declaration of Independence of the United States of America by Thomas Jefferson",
                        "https://www.gutenberg.org/ebooks/730|||Oliver Twist by Charles Dickens",
                        "https://www.gutenberg.org/ebooks/17489|||Les misérables Tome I: Fantine by Victor Hugo",
                        "https://www.gutenberg.org/ebooks/41|||The Legend of Sleepy Hollow by Washington Irving",
                        "https://www.gutenberg.org/ebooks/3207|||Leviathan by Thomas Hobbes",
                        "https://www.gutenberg.org/ebooks/25344|||The Scarlet Letter by Nathaniel Hawthorne",
                        "https://www.gutenberg.org/ebooks/4217|||A Portrait of the Artist as a Young Man by James Joyce",
                        "https://www.gutenberg.org/ebooks/26839|||Mathematical Recreations and Essays by W. W. Rouse Ball",
                        "https://www.gutenberg.org/ebooks/12|||Through the Looking-Glass by Lewis Carroll",
                        "https://www.gutenberg.org/ebooks/5827|||The Problems of Philosophy by Bertrand Russell",
                        "https://www.gutenberg.org/ebooks/19616|||Aesop's Fables - Volume 01 by Aesop",
                        "https://www.gutenberg.org/ebooks/58221|||La Odisea by Homer",
                    ],
                },
            },
            "required": ["recommendation", "reference_url"]
        },
    },
}


json_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "BookRecommendation",
    "type": "object",
    "properties": {
        "recommendation": {
            "type": "string",
            "description": "A recommendation of a book to read with an explanation of why this title was chosen.",
        },
        "reference_url": {
            "type": "string",
            "description": "A URL taken from one of the provided references.",
            "enum": [
                "https://www.gutenberg.org/ebooks/2701",
                "https://www.gutenberg.org/ebooks/145",
                "https://www.gutenberg.org/ebooks/2641",
                "https://www.gutenberg.org/ebooks/100",
                "https://www.gutenberg.org/ebooks/37106",
                "https://www.gutenberg.org/ebooks/16389",
                "https://www.gutenberg.org/ebooks/67979",
                "https://www.gutenberg.org/ebooks/1342",
                "https://www.gutenberg.org/ebooks/6761",
                "https://www.gutenberg.org/ebooks/394",
                "https://www.gutenberg.org/ebooks/6593",
                "https://www.gutenberg.org/ebooks/4085",
                "https://www.gutenberg.org/ebooks/2160",
                "https://www.gutenberg.org/ebooks/5197",
                "https://www.gutenberg.org/ebooks/1259",
                "https://www.gutenberg.org/ebooks/4300",
                "https://www.gutenberg.org/ebooks/84",
                "https://www.gutenberg.org/ebooks/11",
                "https://www.gutenberg.org/ebooks/1080",
                "https://www.gutenberg.org/ebooks/345",
                "https://www.gutenberg.org/ebooks/174",
                "https://www.gutenberg.org/ebooks/2554",
                "https://www.gutenberg.org/ebooks/2000",
                "https://www.gutenberg.org/ebooks/5200",
                "https://www.gutenberg.org/ebooks/28054",
                "https://www.gutenberg.org/ebooks/1661",
                "https://www.gutenberg.org/ebooks/98",
                "https://www.gutenberg.org/ebooks/73838",
                "https://www.gutenberg.org/ebooks/64317",
                "https://www.gutenberg.org/ebooks/14859",
                "https://www.gutenberg.org/ebooks/996",
                "https://www.gutenberg.org/ebooks/76",
                "https://www.gutenberg.org/ebooks/1998",
                "https://www.gutenberg.org/ebooks/6130",
                "https://www.gutenberg.org/ebooks/30254",
                "https://www.gutenberg.org/ebooks/1400",
                "https://www.gutenberg.org/ebooks/2542",
                "https://www.gutenberg.org/ebooks/27827",
                "https://www.gutenberg.org/ebooks/2600",
                "https://www.gutenberg.org/ebooks/2591",
                "https://www.gutenberg.org/ebooks/1260",
                "https://www.gutenberg.org/ebooks/1952",
                "https://www.gutenberg.org/ebooks/5740",
                "https://www.gutenberg.org/ebooks/844",
                "https://www.gutenberg.org/ebooks/1184",
                "https://www.gutenberg.org/ebooks/43",
                "https://www.gutenberg.org/ebooks/31552",
                "https://www.gutenberg.org/ebooks/244",
                "https://www.gutenberg.org/ebooks/16119",
                "https://www.gutenberg.org/ebooks/46",
                "https://www.gutenberg.org/ebooks/1232",
                "https://www.gutenberg.org/ebooks/74",
                "https://www.gutenberg.org/ebooks/2446",
                "https://www.gutenberg.org/ebooks/45",
                "https://www.gutenberg.org/ebooks/219",
                "https://www.gutenberg.org/ebooks/2814",
                "https://www.gutenberg.org/ebooks/10",
                "https://www.gutenberg.org/ebooks/2650",
                "https://www.gutenberg.org/ebooks/73834",
                "https://www.gutenberg.org/ebooks/16",
                "https://www.gutenberg.org/ebooks/2680",
                "https://www.gutenberg.org/ebooks/8492",
                "https://www.gutenberg.org/ebooks/1727",
                "https://www.gutenberg.org/ebooks/67098",
                "https://www.gutenberg.org/ebooks/33283",
                "https://www.gutenberg.org/ebooks/768",
                "https://www.gutenberg.org/ebooks/205",
                "https://www.gutenberg.org/ebooks/58585",
                "https://www.gutenberg.org/ebooks/22091",
                "https://www.gutenberg.org/ebooks/4363",
                "https://www.gutenberg.org/ebooks/1497",
                "https://www.gutenberg.org/ebooks/27509",
                "https://www.gutenberg.org/ebooks/31284",
                "https://www.gutenberg.org/ebooks/158",
                "https://www.gutenberg.org/ebooks/36034",
                "https://www.gutenberg.org/ebooks/135",
                "https://www.gutenberg.org/ebooks/1946",
                "https://www.gutenberg.org/ebooks/36",
                "https://www.gutenberg.org/ebooks/1399",
                "https://www.gutenberg.org/ebooks/120",
                "https://www.gutenberg.org/ebooks/8800",
                "https://www.gutenberg.org/ebooks/55",
                "https://www.gutenberg.org/ebooks/514",
                "https://www.gutenberg.org/ebooks/600",
                "https://www.gutenberg.org/ebooks/398",
                "https://www.gutenberg.org/ebooks/20738",
                "https://www.gutenberg.org/ebooks/73828",
                "https://www.gutenberg.org/ebooks/1",
                "https://www.gutenberg.org/ebooks/730",
                "https://www.gutenberg.org/ebooks/17489",
                "https://www.gutenberg.org/ebooks/41",
                "https://www.gutenberg.org/ebooks/3207",
                "https://www.gutenberg.org/ebooks/25344",
                "https://www.gutenberg.org/ebooks/4217",
                "https://www.gutenberg.org/ebooks/26839",
                "https://www.gutenberg.org/ebooks/12",
                "https://www.gutenberg.org/ebooks/5827",
                "https://www.gutenberg.org/ebooks/19616",
                "https://www.gutenberg.org/ebooks/58221",
            ],
        },
    },
    "required": ["recommendation", "reference_url"]
}


references = [
    {
        "href": "https://www.gutenberg.org/ebooks/2701",
        "title": "Moby Dick; Or, The Whale by Herman Melville (2196)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/145",
        "title": "Middlemarch by George Eliot (1750)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/2641",
        "title": "A Room with a View by E. M.  Forster (1675)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/100",
        "title": "The Complete Works of William Shakespeare by William Shakespeare (1633)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/37106",
        "title": "Little Women; Or, Meg, Jo, Beth, and Amy by Louisa May Alcott (1624)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/16389",
        "title": "The Enchanted April by Elizabeth Von Arnim (1525)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/67979",
        "title": "The Blue Castle: a novel by L. M.  Montgomery (1512)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/1342",
        "title": "Pride and Prejudice by Jane Austen (1434)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/6761",
        "title": "The Adventures of Ferdinand Count Fathom — Complete by T.  Smollett (1421)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/394",
        "title": "Cranford by Elizabeth Cleghorn Gaskell (1420)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/6593",
        "title": "History of Tom Jones, a Foundling by Henry Fielding (1411)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/4085",
        "title": "The Adventures of Roderick Random by T.  Smollett (1378)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/2160",
        "title": "The Expedition of Humphry Clinker by T.  Smollett (1368)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/5197",
        "title": "My Life — Volume 1 by Richard Wagner (1353)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/1259",
        "title": "Twenty years after by Alexandre Dumas and Auguste Maquet (1350)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/4300",
        "title": "Ulysses by James Joyce (1094)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/84",
        "title": "Frankenstein; Or, The Modern Prometheus by Mary Wollstonecraft Shelley (1068)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/11",
        "title": "Alice's Adventures in Wonderland by Lewis Carroll (1017)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/1080",
        "title": "A Modest Proposal by Jonathan Swift (751)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/345",
        "title": "Dracula by Bram Stoker (582)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/174",
        "title": "The Picture of Dorian Gray by Oscar Wilde (574)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/2554",
        "title": "Crime and Punishment by Fyodor Dostoyevsky (553)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/2000",
        "title": "Don Quijote by Miguel de Cervantes Saavedra (525)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/5200",
        "title": "Metamorphosis by Franz Kafka (517)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/28054",
        "title": "The Brothers Karamazov by Fyodor Dostoyevsky (515)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/1661",
        "title": "The Adventures of Sherlock Holmes by Arthur Conan Doyle (503)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/98",
        "title": "A Tale of Two Cities by Charles Dickens (453)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/73838",
        "title": "The Vatican swindle : by André Gide (444)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/64317",
        "title": "The Great Gatsby by F. Scott  Fitzgerald (441)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/14859",
        "title": "Daddy Takes Us to the Garden by Howard Roger Garis (441)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/996",
        "title": "Don Quixote by Miguel de Cervantes Saavedra (432)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/76",
        "title": "Adventures of Huckleberry Finn by Mark Twain (392)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/1998",
        "title": "Thus Spake Zarathustra: A Book for All and None by Friedrich Wilhelm Nietzsche (373)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/6130",
        "title": "The Iliad by Homer (366)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/30254",
        "title": "The Romance of Lust: A classic Victorian erotic novel by Anonymous (363)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/1400",
        "title": "Great Expectations by Charles Dickens (345)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/2542",
        "title": "A Doll's House : a play by Henrik Ibsen (344)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/27827",
        "title": "The Kama Sutra of Vatsyayana by Vatsyayana (332)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/2600",
        "title": "War and Peace by graf Leo Tolstoy (320)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/2591",
        "title": "Grimms' Fairy Tales by Jacob Grimm and Wilhelm Grimm (320)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/1260",
        "title": "Jane Eyre: An Autobiography by Charlotte Brontë (319)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/1952",
        "title": "The Yellow Wallpaper by Charlotte Perkins Gilman (316)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/5740",
        "title": "Tractatus Logico-Philosophicus by Ludwig Wittgenstein (312)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/844",
        "title": "The Importance of Being Earnest: A Trivial Comedy for Serious People by Oscar Wilde (311)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/1184",
        "title": "The Count of Monte Cristo by Alexandre Dumas and Auguste Maquet (310)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/43",
        "title": "The Strange Case of Dr. Jekyll and Mr. Hyde by Robert Louis Stevenson (308)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/31552",
        "title": "Novo dicionário da língua portuguesa by Cândido de Figueiredo (307)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/244",
        "title": "A Study in Scarlet by Arthur Conan Doyle (301)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/16119",
        "title": "Doctrina Christiana (297)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/46",
        "title": "A Christmas Carol in Prose; Being a Ghost Story of Christmas by Charles Dickens (297)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/1232",
        "title": "The Prince by Niccolò Machiavelli (296)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/74",
        "title": "The Adventures of Tom Sawyer, Complete by Mark Twain (294)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/2446",
        "title": "An Enemy of the People by Henrik Ibsen (292)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/45",
        "title": "Anne of Green Gables by L. M.  Montgomery (285)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/219",
        "title": "Heart of Darkness by Joseph Conrad (285)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/2814",
        "title": "Dubliners by James Joyce (277)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/10",
        "title": "The King James Version of the Bible (272)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/2650",
        "title": "Du côté de chez Swann by Marcel Proust (270)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/73834",
        "title": "A first book in organic evolution by D. Kerfoot  Shute (268)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/16",
        "title": "Peter Pan by J. M.  Barrie (268)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/2680",
        "title": "Meditations by Emperor of Rome Marcus Aurelius (263)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/8492",
        "title": "The King in Yellow by Robert W.  Chambers (261)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/1727",
        "title": "The Odyssey by Homer (254)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/67098",
        "title": "Winnie-the-Pooh by A. A.  Milne (247)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/33283",
        "title": "Calculus Made Easy by Silvanus P.  Thompson (243)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/768",
        "title": "Wuthering Heights by Emily Brontë (243)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/205",
        "title": "Walden, and On The Duty Of Civil Disobedience by Henry David Thoreau (243)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/58585",
        "title": "The Prophet by Kahlil Gibran (243)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/22091",
        "title": "The Best Short Stories of 1920, and the Yearbook of the American Short Story (242)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/4363",
        "title": "Beyond Good and Evil by Friedrich Wilhelm Nietzsche (239)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/1497",
        "title": "The Republic by Plato (238)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/27509",
        "title": "The 2006 CIA World Factbook by United States. Central Intelligence Agency (236)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/31284",
        "title": "Josefine Mutzenbacher by Felix Salten (235)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/158",
        "title": "Emma by Jane Austen (234)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/36034",
        "title": "White Nights and Other Stories by Fyodor Dostoyevsky (234)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/135",
        "title": "Les Misérables by Victor Hugo (228)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/1946",
        "title": "On War by Carl von Clausewitz (228)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/36",
        "title": "The War of the Worlds by H. G.  Wells (223)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/1399",
        "title": "Anna Karenina by graf Leo Tolstoy (221)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/120",
        "title": "Treasure Island by Robert Louis Stevenson (221)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/8800",
        "title": "The divine comedy by Dante Alighieri (220)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/55",
        "title": "The Wonderful Wizard of Oz by L. Frank  Baum (219)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/514",
        "title": "Little Women by Louisa May Alcott (217)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/600",
        "title": "Notes from the Underground by Fyodor Dostoyevsky (216)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/398",
        "title": "The First Book of Adam and Eve by Rutherford Hayes Platt (214)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/20738",
        "title": "Diccionario Ingles-Español-Tagalog by Sofronio G. Calderón (213)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/73828",
        "title": "From the Arctic Ocean to the Yellow Sea : by Julius M.  Price (212)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/1",
        "title": "The Declaration of Independence of the United States of America by Thomas Jefferson (209)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/730",
        "title": "Oliver Twist by Charles Dickens (208)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/17489",
        "title": "Les misérables Tome I: Fantine by Victor Hugo (206)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/41",
        "title": "The Legend of Sleepy Hollow by Washington Irving (197)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/3207",
        "title": "Leviathan by Thomas Hobbes (194)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/25344",
        "title": "The Scarlet Letter by Nathaniel Hawthorne (192)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/4217",
        "title": "A Portrait of the Artist as a Young Man by James Joyce (188)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/26839",
        "title": "Mathematical Recreations and Essays by W. W. Rouse  Ball (188)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/12",
        "title": "Through the Looking-Glass by Lewis Carroll (187)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/5827",
        "title": "The Problems of Philosophy by Bertrand Russell (185)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/19616",
        "title": "Aesop's Fables - Volume 01 by Aesop (178)",
    },
    {
        "href": "https://www.gutenberg.org/ebooks/58221",
        "title": "La Odisea by Homer (177)",
    },
]

GPT_TOOL_SCHEMA_JULY = '''
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "GroupedFinancialResources",
  "type": "object",
  "properties": {
    "gaps": {
      "type": "array",
      "description": "An array of gaps the candidates need to overcome",
      "items": {
        "type": "object",
        "properties": {
            "gap_description":{
            "type": "string",
            "description": "The specific gap the candidate needs to overcome"},
          "gap_category": {
            "type": "string",
            "description": "The title of the category"
          },
         "remedial": {
            "type": "string",
            "description": "Explain how these resources will help the candidate overcome a specific gap"
          },          
          "sources": {
            "type": "array",
            "description": "An array of financial resource URLs with metadata",
            "items": {
              "type": "string",
              "description": "A URL from the provided financial resources, appended with the type, title, and description as query parameters",
              "enum": [
                "https://www.wallstreetoasis.com/resources/interviews/investment-banking-interview-questions-answers?type=Investment_Banking_Resources&title=101%20Investment%20Banking%20Interview%20Questions&description=Provides%20a%20comprehensive%20list%20of%20interview%20questions%20commonly%20asked%20in%20investment%20banking%20interviews.",
                "https://www.streetofwalls.com/finance-training-courses/investment-banking-overview-and-behavioral-training/investment-banking-overview?type=Investment_Banking_Resources&title=Investment%20Banking%20Hierarchy&description=Explains%20the%20various%20roles%20and%20structures%20within%20an%20investment%20bank.",
                "https://mergersandinquisitions.com/investment-banking-interview-questions-and-answers/?type=Investment_Banking_Resources&title=Investment%20Banking%20Interview%20Questions%20and%20Answers%3A%20The%20Definitive%20Guide&description=A%20detailed%20guide%20that%20covers%20potential%20questions%20and%20answers%20for%20investment%20banking%20interviews.",
                "https://mergersandinquisitions.com/investment-banking/recruitment/resumes/?type=Investment_Banking_Resources&title=Investment%20Banking%20Resumes&description=Offers%20tips%20and%20examples%20for%20crafting%20an%20effective%20resume%20for%20investment%20banking%20roles.",
                "https://mergersandinquisitions.com/how-to-get-into-investment-banking/#HowToGetIn?type=Investment_Banking_Resources&title=How%20to%20get%20into%20Investment%20Banking&description=Provides%20strategies%20and%20steps%20for%20breaking%20into%20the%20investment%20banking%20industry.",
                "https://www.wallstreetprep.com/knowledge/ma-analyst-day-in-the-life/?type=Investment_Banking_Resources&title=Day%20in%20the%20Life%20of%20an%20IB%20analyst&description=Describes%20a%20typical%20day%20for%20an%20investment%20banking%20analyst%2C%20offering%20insights%20into%20the%20daily%20tasks%20and%20work%20environment.",
                "https://www.investopedia.com/articles/financialcareers/10/investment-banking-interview.asp?type=Investment_Banking_Resources&title=What%20To%20Know%20for%20an%20Investment%20Banking%20Interview&description=Discusses%20key%20topics%20and%20knowledge%20areas%20relevant%20for%20investment%20banking%20interviews.",
                "https://corporatefinanceinstitute.com/resources/career/real-investment-banking-interview-questions-form/?type=Investment_Banking_Resources&title=More%20IB%20interview%20q%26a&description=Collection%20of%20real%20interview%20questions%20and%20answers%20for%20investment%20banking%20job%20candidates.",
                "https://igotanoffer.com/blogs/finance/investment-banking-interview-prep?type=Investment_Banking_Resources&title=Investment%20banking%20interview%20prep%20guide&description=A%20guide%20to%20preparing%20for%20investment%20banking%20interviews%2C%20including%20tips%20on%20how%20to%20answer%20common%20questions.",
                "https://www.indeed.com/career-advice/interviewing/investment-bank-interview-questions?type=Investment_Banking_Resources&title=IB%20interview%20sample%20questions&description=Sample%20questions%20that%20may%20be%20asked%20during%20an%20investment%20banking%20interview%2C%20with%20guidance%20on%20how%20to%20respond.",
                "https://www.streetofwalls.com/articles/private-equity/learn-the-basics/how-private-equity-works/?type=Private_Equity_Resources&title=How%20a%20PE%20Firm%20Works&description=Explains%20the%20fundamental%20operations%20of%20a%20private%20equity%20firm.",
                "https://mergersandinquisitions.com/private-equity/recruitment/?type=Private_Equity_Resources&title=How%20to%20Break%20into%20Private%20Equity&description=Provides%20strategies%20for%20securing%20a%20position%20in%20the%20private%20equity%20sector.",
                "https://www.streetofwalls.com/finance-training-courses/private-equity-training/private-equity-resume/?type=Private_Equity_Resources&title=PE%20Resume&description=Offers%20guidance%20on%20crafting%20a%20resume%20tailored%20for%20private%20equity%20roles.",
                "https://www.wallstreetoasis.com/resources/interviews/private-equity-interview-questions?type=Private_Equity_Resources&title=PE%20Interview%20Questions&description=Features%20a%20list%20of%20common%20interview%20questions%20asked%20during%20PE%20interviews.",
                "https://mergersandinquisitions.com/private-equity-interviews/?type=Private_Equity_Resources&title=Private%20Equity%20Interviews%20101%3A%20How%20to%20Win%20Offers&description=Provides%20a%20guide%20to%20excelling%20in%20private%20equity%20interviews.",
                "https://mergersandinquisitions.com/private-equity/?type=Private_Equity_Resources&title=Private%20Equity%20Overview&description=An%20overview%20of%20the%20private%20equity%20industry%2C%20including%20key%20practices%20and%20challenges.",
                "https://www.wallstreetprep.com/knowledge/lbo-modeling-test-example-solutions/?type=Private_Equity_Resources&title=Basic%20LBO%20Modelling%20Test&description=Introduces%20a%20basic%20leveraged%20buyout%20%28LBO%29%20modeling%20test%20with%20example%20solutions.",
                "https://www.wallstreetprep.com/knowledge/leveraged-buyout-lbo-modeling-1-hour-practice-test/?type=Private_Equity_Resources&title=Standard%20LBO%20Modelling%20Test&description=Provides%20a%20practice%20LBO%20modeling%20test%20designed%20to%20be%20completed%20within%20one%20hour.",
                "https://www.wallstreetprep.com/knowledge/advanced-lbo-modeling-test-4-hour-example/?type=Private_Equity_Resources&title=Advanced%20LBO%20Modelling%20Test&description=Features%20an%20advanced%20LBO%20modeling%20test%20that%20spans%20four%20hours%2C%20intended%20for%20more%20experienced%20professionals.",
                "https://growthequityinterviewguide.com/private-equity-interview-questions?type=Private_Equity_Resources&title=Top%2017%20PE%20Interview%20Questions&description=Lists%20top%2017%20interview%20questions%20specific%20to%20private%20equity%20interviews.",
                "https://www.fe.training/free-resources/careers-in-finance/private-equity-interview-questions/?type=Private_Equity_Resources&title=More%20PE%20Interview%20Questions&description=A%20collection%20of%20additional%20private%20equity%20interview%20questions.",
                "https://readwrite.com/the-art-of-private-equity-interviewing-tips-for-impressive-responses/?type=Private_Equity_Resources&title=Tips%20for%20Impressive%20Responses%20for%20PE%20Interview&description=Offers%20tips%20on%20how%20to%20deliver%20impressive%20responses%20in%20private%20equity%20interviews.",
                "https://transacted.io/private-equity-interview-preparation-guide/?type=Private_Equity_Resources&title=PE%20Interview%20Prep%20Guide&description=A%20comprehensive%20guide%20to%20preparing%20for%20private%20equity%20interviews.",
                "https://www.10xebitda.com/why-private-equity-interview-answer/?type=Private_Equity_Resources&title=How%20to%20Answer%20%E2%80%98Why%20Private%20Equity%E2%80%99&description=Provides%20insights%20on%20how%20to%20effectively%20answer%20common%20questions%20about%20one%27s%20motivation%20for%20pursuing%20a%20career%20in%20private%20equity.",
                "https://www.wallstreetoasis.com/resources/interviews/venture-capital-interview-questions?type=Venture_Capital_Resources&title=VC%20Interview%20Questions&description=A%20list%20of%20common%20questions%20asked%20during%20venture%20capital%20interviews.",
                "https://mergersandinquisitions.com/venture-capital?type=Venture_Capital_Resources&title=VC%20Overview&description=Provides%20a%20broad%20overview%20of%20the%20venture%20capital%20industry%2C%20including%20key%20players%20and%20processes.",
                "https://mergersandinquisitions.com/venture-capital-interview-questions?type=Venture_Capital_Resources&title=Venture%20Capital%20Interview%20Questions%3A%20What%20to%20Expect%20and%20How%20to%20Prepare&description=Detailed%20guide%20on%20what%20to%20expect%20in%20VC%20interviews%20and%20how%20to%20prepare%20effectively.",
                "https://www.wallstreetprep.com/knowledge/venture-capital-diligence/?type=Venture_Capital_Resources&title=Fundamentals%20of%20Early-Stage%20Investing&description=Explains%20the%20due%20diligence%20process%20in%20early-stage%20venture%20capital%20investing.",
                "https://www.investopedia.com/articles/financial-careers/08/venture-capital-interview-questions.asp?type=Venture_Capital_Resources&title=Top%20VC%20Interview%20Questions&description=Outlines%20some%20of%20the%20top%20interview%20questions%20for%20venture%20capital%20job%20applicants.",
                "https://www.goingvc.com/post/the-ultimate-venture-capital-interview-guide?type=Venture_Capital_Resources&title=Ultimate%20VC%20Interview%20Guide&description=Comprehensive%20guide%20to%20succeeding%20in%20venture%20capital%20interviews.",
                "https://www.joinleland.com/library/a/50-most-common-venture-capital-interview-questions?type=Venture_Capital_Resources&title=50%20Most%20Common%20VC%20Interview%20Questions&description=Compiles%20the%2050%20most%20frequently%20asked%20questions%20in%20VC%20interviews.",
                "https://sg.indeed.com/career-advice/interviewing/venture-capital-interview-questions?type=Venture_Capital_Resources&title=37%20VC%20Interview%20Questions%20with%20Answers&description=Provides%20a%20set%20of%2037%20venture%20capital%20interview%20questions%20along%20with%20suggested%20answers.",
                "https://www.wallstreetoasis.com/resources/interviews/hedge-funds-interview-questions?type=Hedge_Fund_Resources&title=Hedge%20Fund%20Interview%20Questions&description=A%20collection%20of%20common%20interview%20questions%20faced%20during%20hedge%20fund%20interviews.",
                "https://www.wallstreetprep.com/knowledge/hedge-fund?type=Hedge_Fund_Resources&title=Hedge%20Fund%20Primer&description=An%20introductory%20guide%20to%20understanding%20the%20basic%20concepts%20and%20strategies%20of%20hedge%20funds.",
                "https://mergersandinquisitions.com/how-to-get-a-job-at-a-hedge-fund/?type=Hedge_Fund_Resources&title=How%20to%20Get%20a%20Job%20at%20a%20Hedge%20Fund&description=Detailed%20strategies%20and%20advice%20for%20landing%20a%20job%20in%20the%20hedge%20fund%20industry.",
                "https://www.streetofwalls.com/articles/hedge-fund/?type=Hedge_Fund_Resources&title=Articles%20on%20Hedge%20Funds&description=A%20compilation%20of%20various%20articles%20providing%20in-depth%20insights%20into%20the%20hedge%20fund%20industry.",
                "https://www.wallstreetmojo.com/hedge-fund-interview-questions/?type=Hedge_Fund_Resources&title=Top%2020%20HF%20Interview%20Q%26A&description=Top%2020%20questions%20and%20answers%20to%20expect%20in%20a%20hedge%20fund%20interview.",
                "https://www.daytrading.com/hedge-fund-interview-questions?type=Hedge_Fund_Resources&title=More%20HF%20Interview%20Q%26A&description=Additional%20hedge%20fund%20interview%20questions%20that%20could%20be%20crucial%20for%20candidates.",
                "https://uk.indeed.com/career-advice/interviewing/hedge-fund-interview-questions?type=Hedge_Fund_Resources&title=40%20Hedge%20Fund%20Interview%20Questions%20%28with%20Sample%20Answers%29&description=A%20robust%20list%20of%2040%20hedge%20fund%20interview%20questions%20along%20with%20guidance%20on%20sample%20answers.",
                "https://www.selbyjennings.com/blog/2023/05/preparing-for-a-hedge-fund-interview-your-comprehensive-guide?type=Hedge_Fund_Resources&title=How%20to%20Prepare%20for%20a%20HF%20Interview&description=A%20comprehensive%20guide%20to%20preparing%20for%20hedge%20fund%20interviews%2C%20covering%20what%20to%20know%20and%20how%20to%20present%20oneself.",
                "https://www.efinancialcareers.sg/news/2023/05/hedge-fund-interview-questions?type=Hedge_Fund_Resources&title=Hedge%20Fund%20Interview%20Questions%3A%20What%20to%20Expect%2C%20and%20What%20to%20Ask&description=Insight%20into%20what%20candidates%20can%20expect%20to%20face%20in%20hedge%20fund%20interviews%20and%20suggestions%20on%20what%20questions%20to%20ask.",
                "https://www.buysidehustle.com/most-frequently-asked-hedge-fund-interview-questions-and-answers/?type=Hedge_Fund_Resources&title=Most%20Frequently%20Asked%20HF%20Interview%20Questions&description=Lists%20the%20most%20frequently%20asked%20questions%20in%20hedge%20fund%20interviews%2C%20complete%20with%20answers.",
                "https://www.wallstreetoasis.com/resources/interviews/accounting-interview-questions?type=Accounting_Resources&title=Accounting%20Interview%20Questions&description=A%20list%20of%20common%20questions%20asked%20during%20accounting%20interviews.",
                "https://www.wallstreetprep.com/knowledge/operating-cash-flow-ocf/?type=Accounting_Resources&title=Fundamentals%20of%20Free%20Cash%20Flow%20%28FCF%29&description=Explains%20the%20basics%20of%20calculating%20and%20analyzing%20free%20cash%20flow%2C%20an%20essential%20concept%20in%20accounting%20and%20finance.",
                "https://www.robertwalters.co.uk/insights/career-advice/blog/five-accounting-interview-tips.html?type=Accounting_Resources&title=Tips%20for%20Accounting%20Interview&description=Provides%20practical%20tips%20to%20excel%20in%20accounting%20interviews%2C%20focusing%20on%20how%20to%20present%20technical%20knowledge%20and%20soft%20skills.",
                "https://www.shiksha.com/online-courses/articles/top-accounting-interview-questions-answers/?type=Accounting_Resources&title=Top%20128%20Accounting%20Interview%20Q%26A&description=A%20comprehensive%20list%20of%20accounting%20interview%20questions%20and%20answers%2C%20covering%20a%20wide%20range%20of%20topics%20in%20the%20field.",
                "https://www.franklin.edu/blog/accounting-mvp/accounting-interview-questions?type=Accounting_Resources&title=How%20to%20Prepare%20for%20Accounting%20Interview&description=Discusses%20strategies%20to%20prepare%20for%20an%20accounting%20interview%2C%20including%20understanding%20what%20recruiters%20are%20looking%20for.",
                "https://accountingsoftwareanswers.com/accounting-interview-questions/?type=Accounting_Resources&title=Guide%20for%20an%20Accounting%20Interview&description=A%20guide%20to%20preparing%20for%20accounting%20interviews%2C%20offering%20insights%20into%20the%20types%20of%20questions%20and%20how%20to%20answer%20them%20effectively.",
                "https://www.sienaheights.edu/how-to-prepare-for-accounting-interview-questions/?type=Accounting_Resources&title=How%20to%20Prepare%20for%20Accounting%20Interview%20Questions&description=Provides%20a%20detailed%20approach%20to%20preparing%20for%20accounting%20interviews%2C%20emphasizing%20the%20importance%20of%20practical%20examples%20to%20illustrate%20accounting%20skills.",
                "https://www.remoterocketship.com/advice/6-risk-analyst-interview-questions-with-sample-answers?type=Risk_Analyst_Resources&title=6%20Risk%20Analyst%20Interview%20Questions%20with%20Sample%20Answers&description=This%20page%20provides%20a%20curated%20list%20of%20interview%20questions%20specifically%20for%20risk%20analyst%20positions%20along%20with%20detailed%20sample%20answers%20to%20help%20candidates%20prepare%20effectively.",
                "https://www.investopedia.com/articles/professionals/111115/common-interview-questions-credit-risk-analysts.asp?type=Risk_Analyst_Resources&title=Common%20Interview%20Questions%3A%20Credit%20Risk%20Analysts&description=Investopedia%20outlines%20common%20interview%20questions%20faced%20by%20credit%20risk%20analysts%2C%20offering%20insights%20into%20the%20skills%20and%20knowledge%20expected%20in%20the%20role.",
                "https://www.ziprecruiter.com/career/job-interview-question-answers/risk-analyst?type=Risk_Analyst_Resources&title=Top%2015%20Risk%20Analyst%20Job%20Interview%20Questions%2C%20Answers%20%26%20Tips&description=ZipRecruiter%20presents%20a%20list%20of%20top%20interview%20questions%20for%20risk%20analysts%2C%20including%20tips%20on%20how%20to%20answer%20and%20what%20employers%20are%20looking%20for.",
                "https://www.indeed.com/career-advice/finding-a-job/how-to-become-risk-analyst?type=Risk_Analyst_Resources&title=How%20To%20Become%20a%20Risk%20Analyst%3A%206%20Steps&description=Indeed%20guides%20on%20the%20steps%20to%20becoming%20a%20risk%20analyst%2C%20detailing%20necessary%20education%2C%20skills%2C%20and%20career%20paths.",
                "https://www.theknowledgeacademy.com/blog/risk-management-interview-questions/?type=Risk_Analyst_Resources&title=Top%2040%20Risk%20Management%20Interview%20Questions&description=The%20Knowledge%20Academy%20provides%20a%20comprehensive%20list%20of%20risk%20management%20interview%20questions%20to%20help%20candidates%20prepare%20for%20interviews%20in%20risk%20management%20roles.",
                "https://www.projectpro.io/article/financial-data-scientist/925?type=IT_Resources&title=How%20to%20Become%20a%20Financial%20Data%20Scientist&description=This%20article%20outlines%20the%20initial%20steps%20necessary%20to%20pursue%20a%20career%20as%20a%20financial%20data%20scientist%2C%20emphasizing%20the%20importance%20of%20mastering%20statistical%20concepts%20and%20analytical%20skills.",
                "https://onlinedegrees.sandiego.edu/data-science-in-finance/?type=IT_Resources&title=Data%20Science%20in%20Finance%20%5BCareer%20Guide%5D&description=The%20guide%20explores%20the%20role%20of%20data%20science%20in%20the%20finance%20sector%2C%20detailing%20the%20skills%20required%20and%20the%20impact%20of%20data%20science%20on%20financial%20strategies%20and%20decisions.",
                "https://www.jobzmall.com/careers/financial-data-scientist/faqs/how-can-i-best-prepare-for-a-career-as-a-financial-data-scientist?type=IT_Resources&title=How%20can%20I%20best%20prepare%20for%20a%20career%20as%20a%20Financial%20Data%20Scientist%3F&description=This%20FAQ%20section%20provides%20insights%20into%20the%20preparations%20necessary%20for%20a%20career%20as%20a%20financial%20data%20scientist%2C%20with%20tips%20on%20education%2C%20skills%20development%2C%20and%20practical%20experience."
              ]
            }
          }
        },
        "required": ["category", "sources"]
      }
    }
  },
  "required": ["categories"]
}
'''
tool_function1 = {
    "name": "gap_remedial_resources",
    "description": "Generate a reference list of resources to help candidates overcome specific gaps",
    "parameters": {
      "type": "object",
      "properties": {
        "gaps": {
          "type": "array",
          "description": "An array of gaps the candidates need to overcome",
          "items": {
            "type": "object",
            "properties": {
              "gap_description": {
                "type": "string",
                "description": "The specific gap the candidate needs to overcome"
              },
              "gap_category": {
                "type": "string",
                "description": "The title of the category"
              },
              "remedial": {
                "type": "string",
                "description": "Explain how these resources will help the candidate overcome a specific gap"
              },
              "sources": {
                "type": "array",
                "description": "An array of financial resource URLs with metadata",
                "items": {
                  "type": "string",
                  "description": "A URL from the provided financial resources, appended with the type, title, and description as query parameters",
                  "enum": [
                    "https://www.wallstreetoasis.com/resources/interviews/investment-banking-interview-questions-answers?type=Investment_Banking_Resources&title=101%20Investment%20Banking%20Interview%20Questions&description=Provides%20a%20comprehensive%20list%20of%20interview%20questions%20commonly%20asked%20in%20investment%20banking%20interviews.",
                    "https://www.streetofwalls.com/finance-training-courses/investment-banking-overview-and-behavioral-training/investment-banking-overview?type=Investment_Banking_Resources&title=Investment%20Banking%20Hierarchy&description=Explains%20the%20various%20roles%20and%20structures%20within%20an%20investment%20bank.",
                    "https://mergersandinquisitions.com/investment-banking-interview-questions-and-answers/?type=Investment_Banking_Resources&title=Investment%20Banking%20Interview%20Questions%20and%20Answers%3A%20The%20Definitive%20Guide&description=A%20detailed%20guide%20that%20covers%20potential%20questions%20and%20answers%20for%20investment%20banking%20interviews.",
                    "https://mergersandinquisitions.com/investment-banking/recruitment/resumes/?type=Investment_Banking_Resources&title=Investment%20Banking%20Resumes&description=Offers%20tips%20and%20examples%20for%20crafting%20an%20effective%20resume%20for%20investment%20banking%20roles.",
                    "https://mergersandinquisitions.com/how-to-get-into-investment-banking/#HowToGetIn?type=Investment_Banking_Resources&title=How%20to%20get%20into%20Investment%20Banking&description=Provides%20strategies%20and%20steps%20for%20breaking%20into%20the%20investment%20banking%20industry.",
                    "https://www.wallstreetprep.com/knowledge/ma-analyst-day-in-the-life/?type=Investment_Banking_Resources&title=Day%20in%20the%20Life%20of%20an%20IB%20analyst&description=Describes%20a%20typical%20day%20for%20an%20investment%20banking%20analyst%2C%20offering%20insights%20into%20the%20daily%20tasks%20and%20work%20environment.",
                    "https://www.investopedia.com/articles/financialcareers/10/investment-banking-interview.asp?type=Investment_Banking_Resources&title=What%20To%20Know%20for%20an%20Investment%20Banking%20Interview&description=Discusses%20key%20topics%20and%20knowledge%20areas%20relevant%20for%20investment%20banking%20interviews.",
                    "https://corporatefinanceinstitute.com/resources/career/real-investment-banking-interview-questions-form/?type=Investment_Banking_Resources&title=More%20IB%20interview%20q%26a&description=Collection%20of%20real%20interview%20questions%20and%20answers%20for%20investment%20banking%20job%20candidates.",
                    "https://igotanoffer.com/blogs/finance/investment-banking-interview-prep?type=Investment_Banking_Resources&title=Investment%20banking%20interview%20prep%20guide&description=A%20guide%20to%20preparing%20for%20investment%20banking%20interviews%2C%20including%20tips%20on%20how%20to%20answer%20common%20questions.",
                    "https://www.indeed.com/career-advice/interviewing/investment-bank-interview-questions?type=Investment_Banking_Resources&title=IB%20interview%20sample%20questions&description=Sample%20questions%20that%20may%20be%20asked%20during%20an%20investment%20banking%20interview%2C%20with%20guidance%20on%20how%20to%20respond.",
                    "https://www.streetofwalls.com/articles/private-equity/learn-the-basics/how-private-equity-works/?type=Private_Equity_Resources&title=How%20a%20PE%20Firm%20Works&description=Explains%20the%20fundamental%20operations%20of%20a%20private%20equity%20firm.",
                    "https://mergersandinquisitions.com/private-equity/recruitment/?type=Private_Equity_Resources&title=How%20to%20Break%20into%20Private%20Equity&description=Provides%20strategies%20for%20securing%20a%20position%20in%20the%20private%20equity%20sector.",
                    "https://www.streetofwalls.com/finance-training-courses/private-equity-training/private-equity-resume/?type=Private_Equity_Resources&title=PE%20Resume&description=Offers%20guidance%20on%20crafting%20a%20resume%20tailored%20for%20private%20equity%20roles.",
                    "https://www.wallstreetoasis.com/resources/interviews/private-equity-interview-questions?type=Private_Equity_Resources&title=PE%20Interview%20Questions&description=Features%20a%20list%20of%20common%20interview%20questions%20asked%20during%20PE%20interviews.",
                    "https://mergersandinquisitions.com/private-equity-interviews/?type=Private_Equity_Resources&title=Private%20Equity%20Interviews%20101%3A%20How%20to%20Win%20Offers&description=Provides%20a%20guide%20to%20excelling%20in%20private%20equity%20interviews.",
                    "https://mergersandinquisitions.com/private-equity/?type=Private_Equity_Resources&title=Private%20Equity%20Overview&description=An%20overview%20of%20the%20private%20equity%20industry%2C%20including%20key%20practices%20and%20challenges.",
                    "https://www.wallstreetprep.com/knowledge/lbo-modeling-test-example-solutions/?type=Private_Equity_Resources&title=Basic%20LBO%20Modelling%20Test&description=Introduces%20a%20basic%20leveraged%20buyout%20%28LBO%29%20modeling%20test%20with%20example%20solutions.",
                    "https://www.wallstreetprep.com/knowledge/leveraged-buyout-lbo-modeling-1-hour-practice-test/?type=Private_Equity_Resources&title=Standard%20LBO%20Modelling%20Test&description=Provides%20a%20practice%20LBO%20modeling%20test%20designed%20to%20be%20completed%20within%20one%20hour.",
                    "https://www.wallstreetprep.com/knowledge/advanced-lbo-modeling-test-4-hour-example/?type=Private_Equity_Resources&title=Advanced%20LBO%20Modelling%20Test&description=Features%20an%20advanced%20LBO%20modeling%20test%20that%20spans%20four%20hours%2C%20intended%20for%20more%20experienced%20professionals.",
                    "https://growthequityinterviewguide.com/private-equity-interview-questions?type=Private_Equity_Resources&title=Top%2017%20PE%20Interview%20Questions&description=Lists%20top%2017%20interview%20questions%20specific%20to%20private%20equity%20interviews.",
                    "https://www.fe.training/free-resources/careers-in-finance/private-equity-interview-questions/?type=Private_Equity_Resources&title=More%20PE%20Interview%20Questions&description=A%20collection%20of%20additional%20private%20equity%20interview%20questions.",
                    "https://readwrite.com/the-art-of-private-equity-interviewing-tips-for-impressive-responses/?type=Private_Equity_Resources&title=Tips%20for%20Impressive%20Responses%20for%20PE%20Interview&description=Offers%20tips%20on%20how%20to%20deliver%20impressive%20responses%20in%20private%20equity%20interviews.",
                    "https://transacted.io/private-equity-interview-preparation-guide/?type=Private_Equity_Resources&title=PE%20Interview%20Prep%20Guide&description=A%20comprehensive%20guide%20to%20preparing%20for%20private%20equity%20interviews.",
                    "https://www.10xebitda.com/why-private-equity-interview-answer/?type=Private_Equity_Resources&title=How%20to%20Answer%20%E2%80%98Why%20Private%20Equity%E2%80%99&description=Provides%20insights%20on%20how%20to%20effectively%20answer%20common%20questions%20about%20one%27s%20motivation%20for%20pursuing%20a%20career%20in%20private%20equity.",
                    "https://www.wallstreetoasis.com/resources/interviews/venture-capital-interview-questions?type=Venture_Capital_Resources&title=VC%20Interview%20Questions&description=A%20list%20of%20common%20questions%20asked%20during%20venture%20capital%20interviews.",
                    "https://mergersandinquisitions.com/venture-capital?type=Venture_Capital_Resources&title=VC%20Overview&description=Provides%20a%20broad%20overview%20of%20the%20venture%20capital%20industry%2C%20including%20key%20players%20and%20processes.",
                    "https://mergersandinquisitions.com/venture-capital-interview-questions?type=Venture_Capital_Resources&title=Venture%20Capital%20Interview%20Questions%3A%20What%20to%20Expect%20and%20How%20to%20Prepare&description=Detailed%20guide%20on%20what%20to%20expect%20in%20VC%20interviews%20and%20how%20to%20prepare%20effectively.",
                    "https://www.wallstreetprep.com/knowledge/venture-capital-diligence/?type=Venture_Capital_Resources&title=Fundamentals%20of%20Early-Stage%20Investing&description=Explains%20the%20due%20diligence%20process%20in%20early-stage%20venture%20capital%20investing.",
                    "https://www.investopedia.com/articles/financial-careers/08/venture-capital-interview-questions.asp?type=Venture_Capital_Resources&title=Top%20VC%20Interview%20Questions&description=Outlines%20some%20of%20the%20top%20interview%20questions%20for%20venture%20capital%20job%20applicants.",
                    "https://www.goingvc.com/post/the-ultimate-venture-capital-interview-guide?type=Venture_Capital_Resources&title=Ultimate%20VC%20Interview%20Guide&description=Comprehensive%20guide%20to%20succeeding%20in%20venture%20capital%20interviews.",
                    "https://www.joinleland.com/library/a/50-most-common-venture-capital-interview-questions?type=Venture_Capital_Resources&title=50%20Most%20Common%20VC%20Interview%20Questions&description=Compiles%20the%2050%20most%20frequently%20asked%20questions%20in%20VC%20interviews.",
                    "https://sg.indeed.com/career-advice/interviewing/venture-capital-interview-questions?type=Venture_Capital_Resources&title=37%20VC%20Interview%20Questions%20with%20Answers&description=Provides%20a%20set%20of%2037%20venture%20capital%20interview%20questions%20along%20with%20suggested%20answers.",
                    "https://www.wallstreetoasis.com/resources/interviews/hedge-funds-interview-questions?type=Hedge_Fund_Resources&title=Hedge%20Fund%20Interview%20Questions&description=A%20collection%20of%20common%20interview%20questions%20faced%20during%20hedge%20fund%20interviews.",
                    "https://www.wallstreetprep.com/knowledge/hedge-fund?type=Hedge_Fund_Resources&title=Hedge%20Fund%20Primer&description=An%20introductory%20guide%20to%20understanding%20the%20basic%20concepts%20and%20strategies%20of%20hedge%20funds.",
                    "https://mergersandinquisitions.com/how-to-get-a-job-at-a-hedge-fund/?type=Hedge_Fund_Resources&title=How%20to%20Get%20a%20Job%20at%20a%20Hedge%20Fund&description=Detailed%20strategies%20and%20advice%20for%20landing%20a%20job%20in%20the%20hedge%20fund%20industry.",
                    "https://www.streetofwalls.com/articles/hedge-fund/?type=Hedge_Fund_Resources&title=Articles%20on%20Hedge%20Funds&description=A%20compilation%20of%20various%20articles%20providing%20in-depth%20insights%20into%20the%20hedge%20fund%20industry.",
                    "https://www.wallstreetmojo.com/hedge-fund-interview-questions/?type=Hedge_Fund_Resources&title=Top%2020%20HF%20Interview%20Q%26A&description=Top%2020%20questions%20and%20answers%20to%20expect%20in%20a%20hedge%20fund%20interview.",
                    "https://www.daytrading.com/hedge-fund-interview-questions?type=Hedge_Fund_Resources&title=More%20HF%20Interview%20Q%26A&description=Additional%20hedge%20fund%20interview%20questions%20that%20could%20be%20crucial%20for%20candidates.",
                    "https://uk.indeed.com/career-advice/interviewing/hedge-fund-interview-questions?type=Hedge_Fund_Resources&title=40%20Hedge%20Fund%20Interview%20Questions%20%28with%20Sample%20Answers%29&description=A%20robust%20list%20of%2040%20hedge%20fund%20interview%20questions%20along%20with%20guidance%20on%20sample%20answers.",
                    "https://www.selbyjennings.com/blog/2023/05/preparing-for-a-hedge-fund-interview-your-comprehensive-guide?type=Hedge_Fund_Resources&title=How%20to%20Prepare%20for%20a%20HF%20Interview&description=A%20comprehensive%20guide%20to%20preparing%20for%20hedge%20fund%20interviews%2C%20covering%20what%20to%20know%20and%20how%20to%20present%20oneself.",
                    "https://www.efinancialcareers.sg/news/2023/05/hedge-fund-interview-questions?type=Hedge_Fund_Resources&title=Hedge%20Fund%20Interview%20Questions%3A%20What%20to%20Expect%2C%20and%20What%20to%20Ask&description=Insight%20into%20what%20candidates%20can%20expect%20to%20face%20in%20hedge%20fund%20interviews%20and%20suggestions%20on%20what%20questions%20to%20ask.",
                    "https://www.buysidehustle.com/most-frequently-asked-hedge-fund-interview-questions-and-answers/?type=Hedge_Fund_Resources&title=Most%20Frequently%20Asked%20HF%20Interview%20Questions&description=Lists%20the%20most%20frequently%20asked%20questions%20in%20hedge%20fund%20interviews%2C%20complete%20with%20answers.",
                    "https://www.wallstreetoasis.com/resources/interviews/accounting-interview-questions?type=Accounting_Resources&title=Accounting%20Interview%20Questions&description=A%20list%20of%20common%20questions%20asked%20during%20accounting%20interviews.",
                    "https://www.wallstreetprep.com/knowledge/operating-cash-flow-ocf/?type=Accounting_Resources&title=Fundamentals%20of%20Free%20Cash%20Flow%20%28FCF%29&description=Explains%20the%20basics%20of%20calculating%20and%20analyzing%20free%20cash%20flow%2C%20an%20essential%20concept%20in%20accounting%20and%20finance.",
                    "https://www.robertwalters.co.uk/insights/career-advice/blog/five-accounting-interview-tips.html?type=Accounting_Resources&title=Tips%20for%20Accounting%20Interview&description=Provides%20practical%20tips%20to%20excel%20in%20accounting%20interviews%2C%20focusing%20on%20how%20to%20present%20technical%20knowledge%20and%20soft%20skills.",
                    "https://www.shiksha.com/online-courses/articles/top-accounting-interview-questions-answers/?type=Accounting_Resources&title=Top%20128%20Accounting%20Interview%20Q%26A&description=A%20comprehensive%20list%20of%20accounting%20interview%20questions%20and%20answers%2C%20covering%20a%20wide%20range%20of%20topics%20in%20the%20field.",
                    "https://www.franklin.edu/blog/accounting-mvp/accounting-interview-questions?type=Accounting_Resources&title=How%20to%20Prepare%20for%20Accounting%20Interview&description=Discusses%20strategies%20to%20prepare%20for%20an%20accounting%20interview%2C%20including%20understanding%20what%20recruiters%20are%20looking%20for.",
                    "https://accountingsoftwareanswers.com/accounting-interview-questions/?type=Accounting_Resources&title=Guide%20for%20an%20Accounting%20Interview&description=A%20guide%20to%20preparing%20for%20accounting%20interviews%2C%20offering%20insights%20into%20the%20types%20of%20questions%20and%20how%20to%20answer%20them%20effectively.",
                    "https://www.sienaheights.edu/how-to-prepare-for-accounting-interview-questions/?type=Accounting_Resources&title=How%20to%20Prepare%20for%20Accounting%20Interview%20Questions&description=Provides%20a%20detailed%20approach%20to%20preparing%20for%20accounting%20interviews%2C%20emphasizing%20the%20importance%20of%20practical%20examples%20to%20illustrate%20accounting%20skills.",
                    "https://www.remoterocketship.com/advice/6-risk-analyst-interview-questions-with-sample-answers?type=Risk_Analyst_Resources&title=6%20Risk%20Analyst%20Interview%20Questions%20with%20Sample%20Answers&description=This%20page%20provides%20a%20curated%20list%20of%20interview%20questions%20specifically%20for%20risk%20analyst%20positions%20along%20with%20detailed%20sample%20answers%20to%20help%20candidates%20prepare%20effectively.",
                    "https://www.investopedia.com/articles/professionals/111115/common-interview-questions-credit-risk-analysts.asp?type=Risk_Analyst_Resources&title=Common%20Interview%20Questions%3A%20Credit%20Risk%20Analysts&description=Investopedia%20outlines%20common%20interview%20questions%20faced%20by%20credit%20risk%20analysts%2C%20offering%20insights%20into%20the%20skills%20and%20knowledge%20expected%20in%20the%20role.",
                    "https://www.ziprecruiter.com/career/job-interview-question-answers/risk-analyst?type=Risk_Analyst_Resources&title=Top%2015%20Risk%20Analyst%20Job%20Interview%20Questions%2C%20Answers%20%26%20Tips&description=ZipRecruiter%20presents%20a%20list%20of%20top%20interview%20questions%20for%20risk%20analysts%2C%20including%20tips%20on%20how%20to%20answer%20and%20what%20employers%20are%20looking%20for.",
                    "https://www.indeed.com/career-advice/finding-a-job/how-to-become-risk-analyst?type=Risk_Analyst_Resources&title=How%20To%20Become%20a%20Risk%20Analyst%3A%206%20Steps&description=Indeed%20guides%20on%20the%20steps%20to%20becoming%20a%20risk%20analyst%2C%20detailing%20necessary%20education%2C%20skills%2C%20and%20career%20paths.",
                    "https://www.theknowledgeacademy.com/blog/risk-management-interview-questions/?type=Risk_Analyst_Resources&title=Top%2040%20Risk%20Management%20Interview%20Questions&description=The%20Knowledge%20Academy%20provides%20a%20comprehensive%20list%20of%20risk%20management%20interview%20questions%20to%20help%20candidates%20prepare%20for%20interviews%20in%20risk%20management%20roles.",
                    "https://www.projectpro.io/article/financial-data-scientist/925?type=IT_Resources&title=How%20to%20Become%20a%20Financial%20Data%20Scientist&description=This%20article%20outlines%20the%20initial%20steps%20necessary%20to%20pursue%20a%20career%20as%20a%20financial%20data%20scientist%2C%20emphasizing%20the%20importance%20of%20mastering%20statistical%20concepts%20and%20analytical%20skills.",
                    "https://onlinedegrees.sandiego.edu/data-science-in-finance/?type=IT_Resources&title=Data%20Science%20in%20Finance%20%5BCareer%20Guide%5D&description=The%20guide%20explores%20the%20role%20of%20data%20science%20in%20the%20finance%20sector%2C%20detailing%20the%20skills%20required%20and%20the%20impact%20of%20data%20science%20on%20financial%20strategies%20and%20decisions.",
                    "https://www.jobzmall.com/careers/financial-data-scientist/faqs/how-can-i-best-prepare-for-a-career-as-a-financial-data-scientist?type=IT_Resources&title=How%20can%20I%20best%20prepare%20for%20a%20career%20as%20a%20Financial%20Data%20Scientist%3F&description=This%20FAQ%20section%20provides%20insights%20into%20the%20preparations%20necessary%20for%20a%20career%20as%20a%20financial%20data%20scientist%2C%20with%20tips%20on%20education%2C%20skills%20development%2C%20and%20practical%20experience."
                  ]
                }
              }
            },
            "required": [
              "category",
              "sources"
            ]
          }
        }
      },
      "required": [
        "categories"
      ]
    }
  }


GPT_TOOL_SCHEMA_JULY2 = '''
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "GroupedFinancialResources",
    "type": "object",
    "properties": {
      "gaps": {
        "type": "array",
        "description": "An array of gaps the candidates need to overcome",
        "items": {
          "type": "object",
          "properties": {
            "gap_description": {
              "type": "string",
              "description": "The specific gap the candidate needs to overcome"
            },
            "gap_category": {
              "type": "string",
              "description": "The title of the category"
            },
            "remedial": {
              "type": "string",
              "description": "Explain how these resources will help the candidate overcome a specific gap"
            },
            "sources": {
              "type": "array",
              "description": "An array of financial resource URLs with metadata",
              "items": {
                "type": "object",
                "properties": {
                  "type": {
                    "type": "string",
                    "description": "The type of the resource"
                  },
                  "title": {
                    "type": "string",
                    "description": "The title of the resource"
                  },
                  "description": {
                    "type": "string",
                    "description": "A brief description of the resource"
                  },
                  "url": {
                    "type": "string",
                    "description": "The URL of the resource"
                  }
                },
                "required": ["type", "title", "description", "url"],
                "enum": [
                  {
                    "type": "Investment_Banking_Resources",
                    "title": "101 Investment Banking Interview Questions",
                    "description": "Provides a comprehensive list of interview questions commonly asked in investment banking interviews.",
                    "url": "https://www.wallstreetoasis.com/resources/interviews/investment-banking-interview-questions-answers"
                  },
                  {
                    "type": "Investment_Banking_Resources",
                    "title": "Investment Banking Hierarchy",
                    "description": "Explains the various roles and structures within an investment bank.",
                    "url": "https://www.streetofwalls.com/finance-training-courses/investment-banking-overview-and-behavioral-training/investment-banking-overview"
                  },
                  {
                    "type": "Investment_Banking_Resources",
                    "title": "Investment Banking Interview Questions and Answers: The Definitive Guide",
                    "description": "A detailed guide that covers potential questions and answers for investment banking interviews.",
                    "url": "https://mergersandinquisitions.com/investment-banking-interview-questions-and-answers/"
                  },
                  {
                    "type": "Investment_Banking_Resources",
                    "title": "Investment Banking Resumes",
                    "description": "Offers tips and examples for crafting an effective resume for investment banking roles.",
                    "url": "https://mergersandinquisitions.com/investment-banking/recruitment/resumes/"
                  },
                  {
                    "type": "Investment_Banking_Resources",
                    "title": "How to get into Investment Banking",
                    "description": "Provides strategies and steps for breaking into the investment banking industry.",
                    "url": "https://mergersandinquisitions.com/how-to-get-into-investment-banking/#HowToGetIn"
                  },
                  {
                    "type": "Investment_Banking_Resources",
                    "title": "Day in the Life of an IB analyst",
                    "description": "Describes a typical day for an investment banking analyst, offering insights into the daily tasks and work environment.",
                    "url": "https://www.wallstreetprep.com/knowledge/ma-analyst-day-in-the-life/"
                  },
                  {
                    "type": "Investment_Banking_Resources",
                    "title": "What To Know for an Investment Banking Interview",
                    "description": "Discusses key topics and knowledge areas relevant for investment banking interviews.",
                    "url": "https://www.investopedia.com/articles/financialcareers/10/investment-banking-interview.asp"
                  },
                  {
                    "type": "Investment_Banking_Resources",
                    "title": "More IB interview q&a",
                    "description": "Collection of real interview questions and answers for investment banking job candidates.",
                    "url": "https://corporatefinanceinstitute.com/resources/career/real-investment-banking-interview-questions-form/"
                  },
                  {
                    "type": "Investment_Banking_Resources",
                    "title": "Investment banking interview prep guide",
                    "description": "A guide to preparing for investment banking interviews, including tips on how to answer common questions.",
                    "url": "https://igotanoffer.com/blogs/finance/investment-banking-interview-prep"
                  },
                  {
                    "type": "Investment_Banking_Resources",
                    "title": "IB interview sample questions",
                    "description": "Sample questions that may be asked during an investment banking interview, with guidance on how to respond.",
                    "url": "https://www.indeed.com/career-advice/interviewing/investment-bank-interview-questions"
                  },
                  {
                    "type": "Private_Equity_Resources",
                    "title": "How a PE Firm Works",
                    "description": "Explains the fundamental operations of a private equity firm.",
                    "url": "https://www.streetofwalls.com/articles/private-equity/learn-the-basics/how-private-equity-works/"
                  },
                  {
                    "type": "Private_Equity_Resources",
                    "title": "How to Break into Private Equity",
                    "description": "Provides strategies for securing a position in the private equity sector.",
                    "url": "https://mergersandinquisitions.com/private-equity/recruitment/"
                  },
                  {
                    "type": "Private_Equity_Resources",
                    "title": "PE Resume",
                    "description": "Offers guidance on crafting a resume tailored for private equity roles.",
                    "url": "https://www.streetofwalls.com/finance-training-courses/private-equity-training/private-equity-resume/"
                  },
                  {
                    "type": "Private_Equity_Resources",
                    "title": "PE Interview Questions",
                    "description": "Features a list of common interview questions asked during PE interviews.",
                    "url": "https://www.wallstreetoasis.com/resources/interviews/private-equity-interview-questions"
                  },
                  {
                    "type": "Private_Equity_Resources",
                    "title": "Private Equity Interviews 101: How to Win Offers",
                    "description": "Provides a guide to excelling in private equity interviews.",
                    "url": "https://mergersandinquisitions.com/private-equity-interviews/"
                  },
                  {
                    "type": "Private_Equity_Resources",
                    "title": "Private Equity Overview",
                    "description": "An overview of the private equity industry, including key practices and challenges.",
                    "url": "https://mergersandinquisitions.com/private-equity/"
                  },
                  {
                    "type": "Private_Equity_Resources",
                    "title": "Basic LBO Modelling Test",
                    "description": "Introduces a basic leveraged buyout (LBO) modeling test with example solutions.",
                    "url": "https://www.wallstreetprep.com/knowledge/lbo-modeling-test-example-solutions/"
                  },
                  {
                    "type": "Private_Equity_Resources",
                    "title": "Standard LBO Modelling Test",
                    "description": "Provides a practice LBO modeling test designed to be completed within one hour.",
                    "url": "https://www.wallstreetprep.com/knowledge/leveraged-buyout-lbo-modeling-1-hour-practice-test/"
                  },
                  {
                    "type": "Private_Equity_Resources",
                    "title": "Advanced LBO Modelling Test",
                    "description": "Features an advanced LBO modeling test that spans four hours, intended for more experienced professionals.",
                    "url": "https://www.wallstreetprep.com/knowledge/advanced-lbo-modeling-test-4-hour-example/"
                  },
                  {
                    "type": "Private_Equity_Resources",
                    "title": "Top 17 PE Interview Questions",
                    "description": "Lists top 17 interview questions specific to private equity interviews.",
                    "url": "https://growthequityinterviewguide.com/private-equity-interview-questions"
                  },
                  {
                    "type": "Private_Equity_Resources",
                    "title": "More PE Interview Questions",
                    "description": "A collection of additional private equity interview questions.",
                    "url": "https://www.fe.training/free-resources/careers-in-finance/private-equity-interview-questions/"
                  },
                  {
                    "type": "Private_Equity_Resources",
                    "title": "Tips for Impressive Responses for PE Interview",
                    "description": "Offers tips on how to deliver impressive responses in private equity interviews.",
                    "url": "https://readwrite.com/the-art-of-private-equity-interviewing-tips-for-impressive-responses/"
                  },
                  {
                    "type": "Private_Equity_Resources",
                    "title": "PE Interview Prep Guide",
                    "description": "A comprehensive guide to preparing for private equity interviews.",
                    "url": "https://transacted.io/private-equity-interview-preparation-guide/"
                  },
                  {
                    "type": "Private_Equity_Resources",
                    "title": "How to Answer ‘Why Private Equity’",
                    "description": "Provides insights on how to effectively answer common questions about one's motivation for pursuing a career in private equity.",
                    "url": "https://www.10xebitda.com/why-private-equity-interview-answer/"
                  },
                  {
                    "type": "Venture_Capital_Resources",
                    "title": "VC Interview Questions",
                    "description": "A list of common questions asked during venture capital interviews.",
                    "url": "https://www.wallstreetoasis.com/resources/interviews/venture-capital-interview-questions"
                  },
                  {
                    "type": "Venture_Capital_Resources",
                    "title": "VC Overview",
                    "description": "Provides a broad overview of the venture capital industry, including key players and processes.",
                    "url": "https://mergersandinquisitions.com/venture-capital"
                  },
                  {
                    "type": "Venture_Capital_Resources",
                    "title": "Venture Capital Interview Questions: What to Expect and How to Prepare",
                    "description": "Detailed guide on what to expect in VC interviews and how to prepare effectively.",
                    "url": "https://mergersandinquisitions.com/venture-capital-interview-questions"
                  },
                  {
                    "type": "Venture_Capital_Resources",
                    "title": "Fundamentals of Early-Stage Investing",
                    "description": "Explains the due diligence process in early-stage venture capital investing.",
                    "url": "https://www.wallstreetprep.com/knowledge/venture-capital-diligence/"
                  },
                  {
                    "type": "Venture_Capital_Resources",
                    "title": "Top VC Interview Questions",
                    "description": "Outlines some of the top interview questions for venture capital job applicants.",
                    "url": "https://www.investopedia.com/articles/financial-careers/08/venture-capital-interview-questions.asp"
                  },
                  {
                    "type": "Venture_Capital_Resources",
                    "title": "Ultimate VC Interview Guide",
                    "description": "Comprehensive guide to succeeding in venture capital interviews.",
                    "url": "https://www.goingvc.com/post/the-ultimate-venture-capital-interview-guide"
                  },
                  {
                    "type": "Venture_Capital_Resources",
                    "title": "50 Most Common VC Interview Questions",
                    "description": "Compiles the 50 most frequently asked questions in VC interviews.",
                    "url": "https://www.joinleland.com/library/a/50-most-common-venture-capital-interview-questions"
                  },
                  {
                    "type": "Venture_Capital_Resources",
                    "title": "37 VC Interview Questions with Answers",
                    "description": "Provides a set of 37 venture capital interview questions along with suggested answers.",
                    "url": "https://sg.indeed.com/career-advice/interviewing/venture-capital-interview-questions"
                  },
                  {
                    "type": "Hedge_Fund_Resources",
                    "title": "Hedge Fund Interview Questions",
                    "description": "A collection of common interview questions faced during hedge fund interviews.",
                    "url": "https://www.wallstreetoasis.com/resources/interviews/hedge-funds-interview-questions"
                  },
                  {
                    "type": "Hedge_Fund_Resources",
                    "title": "Hedge Fund Primer",
                    "description": "An introductory guide to understanding the basic concepts and strategies of hedge funds.",
                    "url": "https://www.wallstreetprep.com/knowledge/hedge-fund"
                  },
                  {
                    "type": "Hedge_Fund_Resources",
                    "title": "How to Get a Job at a Hedge Fund",
                    "description": "Detailed strategies and advice for landing a job in the hedge fund industry.",
                    "url": "https://mergersandinquisitions.com/how-to-get-a-job-at-a-hedge-fund/"
                  },
                  {
                    "type": "Hedge_Fund_Resources",
                    "title": "Articles on Hedge Funds",
                    "description": "A compilation of various articles providing in-depth insights into the hedge fund industry.",
                    "url": "https://www.streetofwalls.com/articles/hedge-fund/"
                  },
                  {
                    "type": "Hedge_Fund_Resources",
                    "title": "Top 20 HF Interview Q&A",
                    "description": "Top 20 questions and answers to expect in a hedge fund interview.",
                    "url": "https://www.wallstreetmojo.com/hedge-fund-interview-questions/"
                  },
                  {
                    "type": "Hedge_Fund_Resources",
                    "title": "More HF Interview Q&A",
                    "description": "Additional hedge fund interview questions that could be crucial for candidates.",
                    "url": "https://www.daytrading.com/hedge-fund-interview-questions"
                  },
                  {
                    "type": "Hedge_Fund_Resources",
                    "title": "40 Hedge Fund Interview Questions (with Sample Answers)",
                    "description": "A robust list of 40 hedge fund interview questions along with guidance on sample answers.",
                    "url": "https://uk.indeed.com/career-advice/interviewing/hedge-fund-interview-questions"
                  },
                  {
                    "type": "Hedge_Fund_Resources",
                    "title": "How to Prepare for a HF Interview",
                    "description": "A comprehensive guide to preparing for hedge fund interviews, covering what to know and how to present oneself.",
                    "url": "https://www.selbyjennings.com/blog/2023/05/preparing-for-a-hedge-fund-interview-your-comprehensive-guide"
                  },
                  {
                    "type": "Hedge_Fund_Resources",
                    "title": "Hedge Fund Interview Questions: What to Expect, and What to Ask",
                    "description": "Insight into what candidates can expect to face in hedge fund interviews and suggestions on what questions to ask.",
                    "url": "https://www.efinancialcareers.sg/news/2023/05/hedge-fund-interview-questions"
                  },
                  {
                    "type": "Hedge_Fund_Resources",
                    "title": "Most Frequently Asked HF Interview Questions",
                    "description": "Lists the most frequently asked questions in hedge fund interviews, complete with answers.",
                    "url": "https://www.buysidehustle.com/most-frequently-asked-hedge-fund-interview-questions-and-answers/"
                  },
                  {
                    "type": "Accounting_Resources",
                    "title": "Accounting Interview Questions",
                    "description": "A list of common questions asked during accounting interviews.",
                    "url": "https://www.wallstreetoasis.com/resources/interviews/accounting-interview-questions"
                  },
                  {
                    "type": "Accounting_Resources",
                    "title": "Fundamentals of Free Cash Flow (FCF)",
                    "description": "Explains the basics of calculating and analyzing free cash flow, an essential concept in accounting and finance.",
                    "url": "https://www.wallstreetprep.com/knowledge/operating-cash-flow-ocf/"
                  },
                  {
                    "type": "Accounting_Resources",
                    "title": "Tips for Accounting Interview",
                    "description": "Provides practical tips to excel in accounting interviews, focusing on how to present technical knowledge and soft skills.",
                    "url": "https://www.robertwalters.co.uk/insights/career-advice/blog/five-accounting-interview-tips.html"
                  },
                  {
                    "type": "Accounting_Resources",
                    "title": "Top 128 Accounting Interview Q&A",
                    "description": "A comprehensive list of accounting interview questions and answers, covering a wide range of topics in the field.",
                    "url": "https://www.shiksha.com/online-courses/articles/top-accounting-interview-questions-answers/"
                  },
                  {
                    "type": "Accounting_Resources",
                    "title": "How to Prepare for Accounting Interview",
                    "description": "Discusses strategies to prepare for an accounting interview, including understanding what recruiters are looking for.",
                    "url": "https://www.franklin.edu/blog/accounting-mvp/accounting-interview-questions"
                  },
                  {
                    "type": "Accounting_Resources",
                    "title": "Guide for an Accounting Interview",
                    "description": "A guide to preparing for accounting interviews, offering insights into the types of questions and how to answer them effectively.",
                    "url": "https://accountingsoftwareanswers.com/accounting-interview-questions/"
                  },
                  {
                    "type": "Accounting_Resources",
                    "title": "How to Prepare for Accounting Interview Questions",
                    "description": "Provides a detailed approach to preparing for accounting interviews, emphasizing the importance of practical examples to illustrate accounting skills.",
                    "url": "https://www.sienaheights.edu/how-to-prepare-for-accounting-interview-questions/"
                  },
                  {
                    "type": "Risk_Analyst_Resources",
                    "title": "6 Risk Analyst Interview Questions with Sample Answers",
                    "description": "This page provides a curated list of interview questions specifically for risk analyst positions along with detailed sample answers to help candidates prepare effectively.",
                    "url": "https://www.remoterocketship.com/advice/6-risk-analyst-interview-questions-with-sample-answers"
                  },
                  {
                    "type": "Risk_Analyst_Resources",
                    "title": "Common Interview Questions: Credit Risk Analysts",
                    "description": "Investopedia outlines common interview questions faced by credit risk analysts, offering insights into the skills and knowledge expected in the role.",
                    "url": "https://www.investopedia.com/articles/professionals/111115/common-interview-questions-credit-risk-analysts.asp"
                  },
                  {
                    "type": "Risk_Analyst_Resources",
                    "title": "Top 15 Risk Analyst Job Interview Questions, Answers & Tips",
                    "description": "ZipRecruiter presents a list of top interview questions for risk analysts, including tips on how to answer and what employers are looking for.",
                    "url": "https://www.ziprecruiter.com/career/job-interview-question-answers/risk-analyst"
                  },
                  {
                    "type": "Risk_Analyst_Resources",
                    "title": "How To Become a Risk Analyst: 6 Steps",
                    "description": "Indeed guides on the steps to becoming a risk analyst, detailing necessary education, skills, and career paths.",
                    "url": "https://www.indeed.com/career-advice/finding-a-job/how-to-become-risk-analyst"
                  },
                  {
                    "type": "Risk_Analyst_Resources",
                    "title": "Top 40 Risk Management Interview Questions",
                    "description": "The Knowledge Academy provides a comprehensive list of risk management interview questions to help candidates prepare for interviews in risk management roles.",
                    "url": "https://www.theknowledgeacademy.com/blog/risk-management-interview-questions/"
                  },
                  {
                    "type": "IT_Resources",
                    "title": "How to Become a Financial Data Scientist",
                    "description": "This article outlines the initial steps necessary to pursue a career as a financial data scientist, emphasizing the importance of mastering statistical concepts and analytical skills.",
                    "url": "https://www.projectpro.io/article/financial-data-scientist/925"
                  },
                  {
                    "type": "IT_Resources",
                    "title": "Data Science in Finance [Career Guide]",
                    "description": "The guide explores the role of data science in the finance sector, detailing the skills required and the impact of data science on financial strategies and decisions.",
                    "url": "https://onlinedegrees.sandiego.edu/data-science-in-finance/"
                  },
                  {
                    "type": "IT_Resources",
                    "title": "How can I best prepare for a career as a Financial Data Scientist?",
                    "description": "This FAQ section provides insights into the preparations necessary for a career as a financial data scientist, with tips on education, skills development, and practical experience.",
                    "url": "https://www.jobzmall.com/careers/financial-data-scientist/faqs/how-can-i-best-prepare-for-a-career-as-a-financial-data-scientist"
                  }
                ]
              }
            }
          },
          "required": ["gap_description", "gap_category", "remedial", "sources"]
        }
      }
    },
    "required": ["gaps"]
  }
'''

LINK_REFERENCES = '''

<REFERENCES>
{
  "resources": [
    {
      "ref": "InvBanRes_0001",
      "type": "Investment_Banking_Resources",
      "title": "101 Investment Banking Interview Questions",
      "description": "Provides a comprehensive list of interview questions commonly asked in investment banking interviews.",
      "url": "https://www.wallstreetoasis.com/resources/interviews/investment-banking-interview-questions-answers"
    },
    {
      "ref": "InvBanRes_0002",
      "type": "Investment_Banking_Resources",
      "title": "Investment Banking Hierarchy",
      "description": "Explains the various roles and structures within an investment bank.",
      "url": "https://www.streetofwalls.com/finance-training-courses/investment-banking-overview-and-behavioral-training/investment-banking-overview"
    },
    {
      "ref": "InvBanRes_0003",
      "type": "Investment_Banking_Resources",
      "title": "Investment Banking Interview Questions and Answers: The Definitive Guide",
      "description": "A detailed guide that covers potential questions and answers for investment banking interviews.",
      "url": "https://mergersandinquisitions.com/investment-banking-interview-questions-and-answers/"
    },
    {
      "ref": "InvBanRes_0004",
      "type": "Investment_Banking_Resources",
      "title": "Investment Banking Resumes",
      "description": "Offers tips and examples for crafting an effective resume for investment banking roles.",
      "url": "https://mergersandinquisitions.com/investment-banking/recruitment/resumes/"
    },
    {
      "ref": "InvBanRes_0005",
      "type": "Investment_Banking_Resources",
      "title": "How to get into Investment Banking",
      "description": "Provides strategies and steps for breaking into the investment banking industry.",
      "url": "https://mergersandinquisitions.com/how-to-get-into-investment-banking/#HowToGetIn"
    },
    {
      "ref": "InvBanRes_0006",
      "type": "Investment_Banking_Resources",
      "title": "Day in the Life of an IB analyst",
      "description": "Describes a typical day for an investment banking analyst, offering insights into the daily tasks and work environment.",
      "url": "https://www.wallstreetprep.com/knowledge/ma-analyst-day-in-the-life/"
    },
    {
      "ref": "InvBanRes_0007",
      "type": "Investment_Banking_Resources",
      "title": "What To Know for an Investment Banking Interview",
      "description": "Discusses key topics and knowledge areas relevant for investment banking interviews.",
      "url": "https://www.investopedia.com/articles/financialcareers/10/investment-banking-interview.asp"
    },
    {
      "ref": "InvBanRes_0008",
      "type": "Investment_Banking_Resources",
      "title": "More IB interview q&a",
      "description": "Collection of real interview questions and answers for investment banking job candidates.",
      "url": "https://corporatefinanceinstitute.com/resources/career/real-investment-banking-interview-questions-form/"
    },
    {
      "ref": "InvBanRes_0009",
      "type": "Investment_Banking_Resources",
      "title": "Investment banking interview prep guide",
      "description": "A guide to preparing for investment banking interviews, including tips on how to answer common questions.",
      "url": "https://igotanoffer.com/blogs/finance/investment-banking-interview-prep"
    },
    {
      "ref": "InvBanRes_0010",
      "type": "Investment_Banking_Resources",
      "title": "IB interview sample questions",
      "description": "Sample questions that may be asked during an investment banking interview, with guidance on how to respond.",
      "url": "https://www.indeed.com/career-advice/interviewing/investment-bank-interview-questions"
    },
    {
      "ref": "PriEquRes_0001",
      "type": "Private_Equity_Resources",
      "title": "How a PE Firm Works",
      "description": "Explains the fundamental operations of a private equity firm.",
      "url": "https://www.streetofwalls.com/articles/private-equity/learn-the-basics/how-private-equity-works/"
    },
    {
      "ref": "PriEquRes_0002",
      "type": "Private_Equity_Resources",
      "title": "How to Break into Private Equity",
      "description": "Provides strategies for securing a position in the private equity sector.",
      "url": "https://mergersandinquisitions.com/private-equity/recruitment/"
    },
    {
      "ref": "PriEquRes_0003",
      "type": "Private_Equity_Resources",
      "title": "PE Resume",
      "description": "Offers guidance on crafting a resume tailored for private equity roles.",
      "url": "https://www.streetofwalls.com/finance-training-courses/private-equity-training/private-equity-resume/"
    },
    {
      "ref": "PriEquRes_0004",
      "type": "Private_Equity_Resources",
      "title": "PE Interview Questions",
      "description": "Features a list of common interview questions asked during PE interviews.",
      "url": "https://www.wallstreetoasis.com/resources/interviews/private-equity-interview-questions"
    },
    {
      "ref": "PriEquRes_0005",
      "type": "Private_Equity_Resources",
      "title": "Private Equity Interviews 101: How to Win Offers",
      "description": "Provides a guide to excelling in private equity interviews.",
      "url": "https://mergersandinquisitions.com/private-equity-interviews/"
    },
    {
      "ref": "PriEquRes_0006",
      "type": "Private_Equity_Resources",
      "title": "Private Equity Overview",
      "description": "An overview of the private equity industry, including key practices and challenges.",
      "url": "https://mergersandinquisitions.com/private-equity/"
    },
    {
      "ref": "PriEquRes_0007",
      "type": "Private_Equity_Resources",
      "title": "Basic LBO Modelling Test",
      "description": "Introduces a basic leveraged buyout (LBO) modeling test with example solutions.",
      "url": "https://www.wallstreetprep.com/knowledge/lbo-modeling-test-example-solutions/"
    },
    {
      "ref": "PriEquRes_0008",
      "type": "Private_Equity_Resources",
      "title": "Standard LBO Modelling Test",
      "description": "Provides a practice LBO modeling test designed to be completed within one hour.",
      "url": "https://www.wallstreetprep.com/knowledge/leveraged-buyout-lbo-modeling-1-hour-practice-test/"
    },
    {
      "ref": "PriEquRes_0009",
      "type": "Private_Equity_Resources",
      "title": "Advanced LBO Modelling Test",
      "description": "Features an advanced LBO modeling test that spans four hours, intended for more experienced professionals.",
      "url": "https://www.wallstreetprep.com/knowledge/advanced-lbo-modeling-test-4-hour-example/"
    },
    {
      "ref": "PriEquRes_0010",
      "type": "Private_Equity_Resources",
      "title": "Top 17 PE Interview Questions",
      "description": "Lists top 17 interview questions specific to private equity interviews.",
      "url": "https://growthequityinterviewguide.com/private-equity-interview-questions"
    },
    {
      "ref": "VenCapRes_0001",
      "type": "Venture_Capital_Resources",
      "title": "VC Interview Questions",
      "description": "A list of common questions asked during venture capital interviews.",
      "url": "https://www.wallstreetoasis.com/resources/interviews/venture-capital-interview-questions"
    },
    {
      "ref": "VenCapRes_0002",
      "type": "Venture_Capital_Resources",
      "title": "VC Overview",
      "description": "Provides a broad overview of the venture capital industry, including key players and processes.",
      "url": "https://mergersandinquisitions.com/venture-capital"
    },
    {
      "ref": "VenCapRes_0003",
      "type": "Venture_Capital_Resources",
      "title": "Venture Capital Interview Questions: What to Expect and How to Prepare",
      "description": "Detailed guide on what to expect in VC interviews and how to prepare effectively.",
      "url": "https://mergersandinquisitions.com/venture-capital-interview-questions"
    },
    {
      "ref": "VenCapRes_0004",
      "type": "Venture_Capital_Resources",
      "title": "Fundamentals of Early-Stage Investing",
      "description": "Explains the due diligence process in early-stage venture capital investing.",
      "url": "https://www.wallstreetprep.com/knowledge/venture-capital-diligence/"
    },
    {
      "ref": "VenCapRes_0005",
      "type": "Venture_Capital_Resources",
      "title": "Top VC Interview Questions",
      "description": "Outlines some of the top interview questions for venture capital job applicants.",
      "url": "https://www.investopedia.com/articles/financial-careers/08/venture-capital-interview-questions.asp"
    },
    {
      "ref": "VenCapRes_0006",
      "type": "Venture_Capital_Resources",
      "title": "Ultimate VC Interview Guide",
      "description": "Comprehensive guide to succeeding in venture capital interviews.",
      "url": "https://www.goingvc.com/post/the-ultimate-venture-capital-interview-guide"
    },
    {
      "ref": "VenCapRes_0007",
      "type": "Venture_Capital_Resources",
      "title": "50 Most Common VC Interview Questions",
      "description": "Compiles the 50 most frequently asked questions in VC interviews.",
      "url": "https://www.joinleland.com/library/a/50-most-common-venture-capital-interview-questions"
    },
    {
      "ref": "VenCapRes_0008",
      "type": "Venture_Capital_Resources",
      "title": "37 VC Interview Questions with Answers",
      "description": "Provides a set of 37 venture capital interview questions along with suggested answers.",
      "url": "https://sg.indeed.com/career-advice/interviewing/venture-capital-interview-questions"
    },
    {
      "ref": "HedFunRes_0001",
      "type": "Hedge_Fund_Resources",
      "title": "Hedge Fund Interview Questions",
      "description": "A collection of common interview questions faced during hedge fund interviews.",
      "url": "https://www.wallstreetoasis.com/resources/interviews/hedge-funds-interview-questions"
    },
    {
      "ref": "HedFunRes_0002",
      "type": "Hedge_Fund_Resources",
      "title": "Hedge Fund Primer",
      "description": "An introductory guide to understanding the basic concepts and strategies of hedge funds.",
      "url": "https://www.wallstreetprep.com/knowledge/hedge-fund"
    },
    {
      "ref": "HedFunRes_0003",
      "type": "Hedge_Fund_Resources",
      "title": "How to Get a Job at a Hedge Fund",
      "description": "Detailed strategies and advice for landing a job in the hedge fund industry.",
      "url": "https://mergersandinquisitions.com/how-to-get-a-job-at-a-hedge-fund/"
    },
    {
      "ref": "HedFunRes_0004",
      "type": "Hedge_Fund_Resources",
      "title": "Articles on Hedge Funds",
      "description": "A compilation of various articles providing in-depth insights into the hedge fund industry.",
      "url": "https://www.streetofwalls.com/articles/hedge-fund/"
    },
    {
      "ref": "HedFunRes_0005",
      "type": "Hedge_Fund_Resources",
      "title": "Top 20 HF Interview Q&A",
      "description": "Top 20 questions and answers to expect in a hedge fund interview.",
      "url": "https://www.wallstreetmojo.com/hedge-fund-interview-questions/"
    },
    {
      "ref": "HedFunRes_0006",
      "type": "Hedge_Fund_Resources",
      "title": "More HF Interview Q&A",
      "description": "Additional hedge fund interview questions that could be crucial for candidates.",
      "url": "https://www.daytrading.com/hedge-fund-interview-questions"
    },
    {
      "ref": "HedFunRes_0007",
      "type": "Hedge_Fund_Resources",
      "title": "40 Hedge Fund Interview Questions (with Sample Answers)",
      "description": "A robust list of 40 hedge fund interview questions along with guidance on sample answers.",
      "url": "https://uk.indeed.com/career-advice/interviewing/hedge-fund-interview-questions"
    },
    {
      "ref": "HedFunRes_0008",
      "type": "Hedge_Fund_Resources",
      "title": "How to Prepare for a HF Interview",
      "description": "A comprehensive guide to preparing for hedge fund interviews, covering what to know and how to present oneself.",
      "url": "https://www.selbyjennings.com/blog/2023/05/preparing-for-a-hedge-fund-interview-your-comprehensive-guide"
    },
    {
      "ref": "HedFunRes_0009",
      "type": "Hedge_Fund_Resources",
      "title": "Hedge Fund Interview Questions: What to Expect, and What to Ask",
      "description": "Insight into what candidates can expect to face in hedge fund interviews and suggestions on what questions to ask.",
      "url": "https://www.efinancialcareers.sg/news/2023/05/hedge-fund-interview-questions"
    },
    {
      "ref": "HedFunRes_0010",
      "type": "Hedge_Fund_Resources",
      "title": "Most Frequently Asked HF Interview Questions",
      "description": "Lists the most frequently asked questions in hedge fund interviews, complete with answers.",
      "url": "https://www.buysidehustle.com/most-frequently-asked-hedge-fund-interview-questions-and-answers/"
    },
    {
      "ref": "AccRes_0001",
      "type": "Accounting_Resources",
      "title": "Accounting Interview Questions",
      "description": "A list of common questions asked during accounting interviews.",
      "url": "https://www.wallstreetoasis.com/resources/interviews/accounting-interview-questions"
    },
    {
      "ref": "AccRes_0002",
      "type": "Accounting_Resources",
      "title": "Fundamentals of Free Cash Flow (FCF)",
      "description": "Explains the basics of calculating and analyzing free cash flow, an essential concept in accounting and finance.",
      "url": "https://www.wallstreetprep.com/knowledge/operating-cash-flow-ocf/"
    },
    {
      "ref": "AccRes_0003",
      "type": "Accounting_Resources",
      "title": "Tips for Accounting Interview",
      "description": "Provides practical tips to excel in accounting interviews, focusing on how to present technical knowledge and soft skills.",
      "url": "https://www.robertwalters.co.uk/insights/career-advice/blog/five-accounting-interview-tips.html"
    },
    {
      "ref": "AccRes_0004",
      "type": "Accounting_Resources",
      "title": "Top 128 Accounting Interview Q&A",
      "description": "A comprehensive list of accounting interview questions and answers, covering a wide range of topics in the field.",
      "url": "https://www.shiksha.com/online-courses/articles/top-accounting-interview-questions-answers/"
    },
    {
      "ref": "AccRes_0005",
      "type": "Accounting_Resources",
      "title": "How to Prepare for Accounting Interview",
      "description": "Discusses strategies to prepare for an accounting interview, including understanding what recruiters are looking for.",
      "url": "https://www.franklin.edu/blog/accounting-mvp/accounting-interview-questions"
    },
    {
      "ref": "AccRes_0006",
      "type": "Accounting_Resources",
      "title": "Guide for an Accounting Interview",
      "description": "A guide to preparing for accounting interviews, offering insights into the types of questions and how to answer them effectively.",
      "url": "https://accountingsoftwareanswers.com/accounting-interview-questions/"
    },
    {
      "ref": "AccRes_0007",
      "type": "Accounting_Resources",
      "title": "How to Prepare for Accounting Interview Questions",
      "description": "Provides a detailed approach to preparing for accounting interviews, emphasizing the importance of practical examples to illustrate accounting skills.",
      "url": "https://www.sienaheights.edu/how-to-prepare-for-accounting-interview-questions/"
    },
    {
      "ref": "RisAnaRes_0001",
      "type": "Risk_Analyst_Resources",
      "title": "6 Risk Analyst Interview Questions with Sample Answers",
      "description": "This page provides a curated list of interview questions specifically for risk analyst positions along with detailed sample answers to help candidates prepare effectively.",
      "url": "https://www.remoterocketship.com/advice/6-risk-analyst-interview-questions-with-sample-answers"
    },
    {
      "ref": "RisAnaRes_0002",
      "type": "Risk_Analyst_Resources",
      "title": "Common Interview Questions: Credit Risk Analysts",
      "description": "Investopedia outlines common interview questions faced by credit risk analysts, offering insights into the skills and knowledge expected in the role.",
      "url": "https://www.investopedia.com/articles/professionals/111115/common-interview-questions-credit-risk-analysts.asp"
    },
    {
      "ref": "RisAnaRes_0003",
      "type": "Risk_Analyst_Resources",
      "title": "Top 15 Risk Analyst Job Interview Questions, Answers & Tips",
      "description": "ZipRecruiter presents a list of top interview questions for risk analysts, including tips on how to answer and what employers are looking for.",
      "url": "https://www.ziprecruiter.com/career/job-interview-question-answers/risk-analyst"
    },
    {
      "ref": "RisAnaRes_0004",
      "type": "Risk_Analyst_Resources",
      "title": "How To Become a Risk Analyst: 6 Steps",
      "description": "Indeed guides on the steps to becoming a risk analyst, detailing necessary education, skills, and career paths.",
      "url": "https://www.indeed.com/career-advice/finding-a-job/how-to-become-risk-analyst"
    },
    {
      "ref": "RisAnaRes_0005",
      "type": "Risk_Analyst_Resources",
      "title": "Top 40 Risk Management Interview Questions",
      "description": "The Knowledge Academy provides a comprehensive list of risk management interview questions to help candidates prepare for interviews in risk management roles.",
      "url": "https://www.theknowledgeacademy.com/blog/risk-management-interview-questions/"
    },
    {
      "ref": "ITRes_0001",
      "type": "IT_Resources",
      "title": "How to Become a Financial Data Scientist",
      "description": "This article outlines the initial steps necessary to pursue a career as a financial data scientist, emphasizing the importance of mastering statistical concepts and analytical skills.",
      "url": "https://www.projectpro.io/article/financial-data-scientist/925"
    },
    {
      "ref": "ITRes_0002",
      "type": "IT_Resources",
      "title": "Data Science in Finance [Career Guide]",
      "description": "The guide explores the role of data science in the finance sector, detailing the skills required and the impact of data science on financial strategies and decisions.",
      "url": "https://onlinedegrees.sandiego.edu/data-science-in-finance/"
    },
    {
      "ref": "ITRes_0003",
      "type": "IT_Resources",
      "title": "How can I best prepare for a career as a Financial Data Scientist?",
      "description": "This FAQ section provides insights into the preparations necessary for a career as a financial data scientist, with tips on education, skills development, and practical experience.",
      "url": "https://www.jobzmall.com/careers/financial-data-scientist/faqs/how-can-i-best-prepare-for-a-career-as-a-financial-data-scientist"
    }
  ]
}
</REFERENCES>

'''

GPT_TOOL_SCHEMA_JULY3 = '''
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "GroupedFinancialResources",
  "type": "object",
  "properties": {
    "gaps": {
      "type": "array",
      "description": "An array of gaps the candidates need to overcome",
      "items": {
        "type": "object",
        "properties": {
            "gap_description":{
            "type": "string",
            "description": "The specific gap the candidate needs to overcome"},
          "gap_category": {
            "type": "string",
            "description": "The title of the category"
          },
         "remedial": {
            "type": "string",
            "description": "Explain how these resources will help the candidate overcome a specific gap"
          },          
          "sources": {
            "type": "array",
            "description": "An array of financial resource URLs with metadata",
            "items": {
              "type": "string",
              "description": "A reference to a financial resource URL with metadata",
              "enum": [
                "InvBanRes_0001",
                "InvBanRes_0002",
                "InvBanRes_0003",
                "InvBanRes_0004",
                "InvBanRes_0005",
                "InvBanRes_0006",
                "InvBanRes_0007",
                "InvBanRes_0008",
                "InvBanRes_0009",
                "InvBanRes_0010",
                "PriEquRes_0001",
                "PriEquRes_0002",
                "PriEquRes_0003",
                "PriEquRes_0004",
                "PriEquRes_0005",
                "PriEquRes_0006",
                "PriEquRes_0007",
                "PriEquRes_0008",
                "PriEquRes_0009",
                "PriEquRes_0010",
                "VenCapRes_0001",
                "VenCapRes_0002",
                "VenCapRes_0003",
                "VenCapRes_0004",
                "VenCapRes_0005",
                "VenCapRes_0006",
                "VenCapRes_0007",
                "VenCapRes_0008",
                "VenCapRes_0009",
                "VenCapRes_0010",
                "HedFunRes_0001",
                "HedFunRes_0002",
                "HedFunRes_0003",
                "HedFunRes_0004",
                "HedFunRes_0005",
                "HedFunRes_0006",
                "HedFunRes_0007",
                "HedFunRes_0008",
                "HedFunRes_0009",
                "HedFunRes_0010",
                "AccRes_0001",
                "AccRes_0002",
                "AccRes_0003",
                "AccRes_0004",
                "AccRes_0005",
                "AccRes_0006",
                "AccRes_0007",
                "AccRes_0008",
                "AccRes_0009",
                "AccRes_0010",
                "RisAnaRes_0001",
                "RisAnaRes_0002",
                "RisAnaRes_0003",
                "RisAnaRes_0004",
                "RisAnaRes_0005",
                "ITRes_0001",
                "ITRes_0002",
                "ITRes_0003"
              ]
            }
          },
        "reasonings": {
            "type": "array",
            "description": "An array of reasons why these resources are relevant",
            "items": {
                "type": "string"
                }
            }
        },
        "required": ["gap_description","gap_category","remedial","sources", "reasonings"]
      }
    }
  },
  "required": ["categories"]
}
'''


GPT_TOOL_SCHEMA_JULY4 = '''
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "GroupedFinancialResources",
  "type": "object",
  "properties": {
    "gap_list": {
      "type": "array",
      "description": "An array listing all the identified gaps the candidates need to overcome",
      "items": {
        "type": "string",
        "description": "A gap the candidate needs to overcome"
      }
    },
    "remedial_resources": {
      "type": "array",
      "description": "An array of objects, each containing information about a financial resource",
      "items": {
        "type": "object",
        "properties": {
          "gap": {
            "type": "string",
            "description": "The specific gap the candidate needs to overcome"
          },
          "gap_category": {
            "type": "string",
            "description": "The title of the category"
          },
          "remedial": {
            "type": "string",
            "description": "Explain how these resources will help the candidate overcome a specific gap"
          },
          "sources": {
            "type": "array",
            "description": "An array of financial resource URLs with metadata",
            "items": {
              "type": "string",
              "description": "A reference to a financial resource URL with metadata",
              "enum": [
                "InvBanRes_0001",
                "InvBanRes_0002",
                "InvBanRes_0003",
                "InvBanRes_0004",
                "InvBanRes_0005",
                "InvBanRes_0006",
                "InvBanRes_0007",
                "InvBanRes_0008",
                "InvBanRes_0009",
                "InvBanRes_0010",
                "PriEquRes_0001",
                "PriEquRes_0002",
                "PriEquRes_0003",
                "PriEquRes_0004",
                "PriEquRes_0005",
                "PriEquRes_0006",
                "PriEquRes_0007",
                "PriEquRes_0008",
                "PriEquRes_0009",
                "PriEquRes_0010",
                "VenCapRes_0001",
                "VenCapRes_0002",
                "VenCapRes_0003",
                "VenCapRes_0004",
                "VenCapRes_0005",
                "VenCapRes_0006",
                "VenCapRes_0007",
                "VenCapRes_0008",
                "VenCapRes_0009",
                "VenCapRes_0010",
                "HedFunRes_0001",
                "HedFunRes_0002",
                "HedFunRes_0003",
                "HedFunRes_0004",
                "HedFunRes_0005",
                "HedFunRes_0006",
                "HedFunRes_0007",
                "HedFunRes_0008",
                "HedFunRes_0009",
                "HedFunRes_0010",
                "AccRes_0001",
                "AccRes_0002",
                "AccRes_0003",
                "AccRes_0004",
                "AccRes_0005",
                "AccRes_0006",
                "AccRes_0007",
                "AccRes_0008",
                "AccRes_0009",
                "AccRes_0010",
                "RisAnaRes_0001",
                "RisAnaRes_0002",
                "RisAnaRes_0003",
                "RisAnaRes_0004",
                "RisAnaRes_0005",
                "ITRes_0001",
                "ITRes_0002",
                "ITRes_0003"
              ]
            }
          },
          "reasonings": {
            "type": "array",
            "description": "An array of reasons why these resources are relevant",
            "items": {
              "type": "string"
            }
          }
        },
        "required": ["gap", "gap_category", "remedial", "sources", "reasonings"]
      }
    }
  },
  "required": ["gap_list","remedial_resources"]
}
'''
