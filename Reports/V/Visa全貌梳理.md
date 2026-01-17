# Visa 全貌梳理

<!-- Generated: 2026-01-16T15:34:38 -->
<!-- Base: /Users/leo/Documents/_3 学习笔记/filings/V -->

**风险警示与免责声明**：*本文由AI/大模型基于 Visa (V) 已公开披露且可核查的财报/公告文件（包括但不限于年度报告、半年度报告、季度报告及其他监管披露文件）与公司官网等公开信息辅助生成，仅用于学术研究与信息交流之目的，因AI/大模型存在幻觉，本文不可避免地会产生不完全符合财报原文的情况，严重程度视AI/大模型的幻觉程度而定，阅读本文后产生的任何观点需核对原文，使用本文内容所产生的任何直接或间接后果，均由使用者自行承担。*



---

## 投资要点概览

### 结论要点

- 核心业务与分部：以 VisaNet 为底座的全球支付网络与交易处理服务，产品与服务按消费支付（CP）、商业与资金流动解决方案（CMS，含 Visa Direct）、增值服务（VAS）组织；公司强调其不发卡、不放贷、不为持卡人设定利率与费用。（对应章节：公司介绍与沿革、产品与服务及护城河）
- 核心产品/服务与定价计费方式：净收入由服务收入、数据处理收入、国际交易收入与其他收入构成，并以客户激励（client incentives）抵减；对价以可变为主，服务收入存在“当季定价×上季支付量”的季度计量特征。（对应章节：收入结构与商业模式、关键经营指标（KPI）与口径字典）
- 核心客户/用户画像与集中度要点：生态以发卡行/收单机构为直接客户，FY2025 披露近 14,500 家金融机构客户、近 50 亿支付凭证、覆盖全球超 1.75 亿商户受理点；净收入口径下各期均有单一客户贡献 11%。（对应章节：用户与客户发展、获客与分发渠道（直销／平台／合作伙伴））
- 核心KPI现状与趋势：KPI 框架包括 payments volume、processed transactions、cross-border volume（ex-Europe）、payment credentials、merchant locations、Tap to Pay 渗透；FY2025 total payments and cash volume 为 $17 trillion，Tap to Pay 在面对面交易中占比全球 79%/美国 66%；VTS 已 provisioned 160 亿 tokens；Visa Direct 2025 财年处理超过 125 亿笔交易。（对应章节：关键经营指标（KPI）与口径字典、未来产品规划与商业规划、产品与服务及护城河）
- 核心财务指标现状与趋势：FY2020–FY2025 净收入由 21,846 百万美元增至 40,000 百万美元（FY2025 同比 +11.3%）；FY2025 运营利润率 60.0%、归母净利润率 50.1%；FY2025 经营现金流 23,059 百万美元。（对应章节：财务表现与盈利能力）
- 重大事项与风险披露要点：FY2025 期末累计诉讼准备金 $3,033 million，其中 U.S. covered litigation $2,698 million，主要与 interchange MDL 相关；DOJ 于 2024-09-24 提起 Sherman Act 诉讼且撤诉动议被驳回；风险因素覆盖监管演进、竞争、结算赔付义务、网络/系统中断与网络安全等。（对应章节：重大诉讼与法律程序、风险分析）

### 买方跟踪清单

- Payments volume（含 Nominal）
  - 定义/口径：Visa 体系相关品牌（Visa/Visa Electron/V PAY/Interlink）的购买交易汇总金额；Nominal 以既定汇率折算为美元。
  - 影响路径：payments volume 是服务收入的核心驱动变量，且与 client incentives 的规模变化具有联动。（基于 MD&A 口径）
  - 触发条件/阈值：payments volume 与净收入/服务收入增速出现持续背离，或季度间结构变化导致“当季定价×上季支付量”的滞后效应放大。
  - 风险情景/敏感点：payments volume 变化与 client incentives 抵减强度变化叠加，净收入弹性与经营现金流波动可能被放大。
  - 验证路径：SEC EDGAR | Form 10-K/10-Q | Item 7. MD&A（payments volume、service revenue、client incentives相关表述）
  - 更新频率：季度

- Processed transactions
  - 定义/口径：Visa 网络处理的支付与现金交易笔数（含 Visa/Visa Electron/V PAY/Interlink/PLUS）。
  - 影响路径：processed transactions 是数据处理收入的核心驱动变量。（基于 MD&A 口径）
  - 触发条件/阈值：交易笔数增速与支付金额增速持续背离（交易结构变化），或交易处理相关风险事件扰动业务连续性。
  - 风险情景/敏感点：交易结构变化可能改变每单位业务量的变现结构与成本侧压力。
  - 验证路径：SEC EDGAR | Form 10-K/10-Q | Item 7. MD&A（processed transactions、data processing revenue相关表述）
  - 更新频率：季度

-（Nominal）Cross-border volume（ex-Europe）
  - 定义/口径：用于解释国际交易收入变动的名义跨境交易量（剔除欧洲区内交易）；正式定义在已检索范围内未见明确“定义/公式”条款，仅作为解释变量被使用。
  - 影响路径：cross-border volume（ex-Europe）用于解释 international transaction revenue 的变化。（基于 MD&A 口径）
  - 触发条件/阈值：跨境交易量/结构变化导致国际交易收入弹性变化，或监管/合规要求改变跨境处理方式与客户接口要求。
  - 风险情景/敏感点：跨境场景对监管、合规与地缘政治更敏感，可能放大波动。
  - 验证路径：SEC EDGAR | Form 10-K/10-Q | Item 7. MD&A（international transaction revenue 与 cross-border volume 表述）、Item 1A（监管风险）
  - 更新频率：季度/事件驱动

- 诉讼准备金与托管资金安排（accrued litigation / litigation escrow）
  - 定义/口径：诉讼与监管事项的计量、计提与支付，及与 U.S./Europe 回溯性责任相关的安排。
  - 影响路径：诉讼计提与支付影响利润表与现金流，并可能通过规则/费率/合规要求对商业条款形成外溢影响。
  - 触发条件/阈值：新增大额计提、和解/判决关键节点、重大调查/诉讼程序进展变化。
  - 风险情景/敏感点：反垄断与费率/规则相关争议的结果可能影响经营条款与成本结构。
  - 验证路径：SEC EDGAR | Form 10-K | Item 8 | Note 20—Legal Matters；Note 5—U.S. and Europe Retrospective Responsibility Plans；Item 3
  - 更新频率：事件驱动/年度

### 详细情况

- 商业模式与变现框架
  - 交易处理服务围绕授权、清算与结算展开，直接客户为发卡机构与收单机构，净收入主要来自 issuer/acquirer。
  - 净收入由服务收入、数据处理收入、国际交易收入与其他收入构成，并以 client incentives 抵减；服务收入的季度计量存在“当季定价×上季支付量”的滞后特征。

- 规模与能力底座（FY2025）
  - 经营规模：total payments and cash volume 为 $17 trillion；近 5 billion payment credentials；more than 175 million merchant locations；近 14,500 家金融机构客户。
  - 能力组件：提供 200+ 项产品与服务；VTS 已 provisioned 160 亿 tokens；Visa Direct 潜在触达约 120 亿端点，2025 财年处理超过 125 亿笔交易、服务超过 650 个合作伙伴。
  - 采用率与体验迁移：Tap to Pay 在面对面交易中占比全球 79%、美国 66%。

- 财务与资本配置（FY2020–FY2025）
  - 净收入与现金流：FY2025 净收入 40,000 百万美元、经营现金流 23,059 百万美元；利润率水平在 FY2025 出现回落（运营利润率 60.0%，归母净利润率 50.1%）。
  - 股东回报：FY2020–FY2025 同时进行分红与回购；FY2025 回购现金支出 18,316,000,000 美元、现金股息支付额 4,634,000,000 美元；截至 2025-09-30 回购剩余额度 $24.9 billion。

- 主要风险与不确定性（以披露为准）
  - 诉讼与调查：FY2025 期末累计诉讼准备金 $3,033 million，其中 U.S. covered litigation $2,698 million；DOJ Sherman Act 诉讼与相关集体诉讼推进带来不确定性。
  - 监管与竞争：风险因素覆盖全球监管演进、行业竞争、卖方与处理商降低受理成本压力等。
  - 结算与网络安全：公司提示结算赔付义务、网络/系统中断与网络安全事件等可能对经营与流动性造成不利影响。

### 证据与出处

- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Part I, Item 1. Business — Overview / Our Core Business（VisaNet、业务边界、规模口径、Tap to Pay、VTS、Visa Direct 等）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations — Payments volume and processed transactions; Net Revenue（KPI 定义与驱动关系、cross-border volume（ex-Europe）用于解释国际交易收入、client incentives 相关表述）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 8. Financial Statements and Supplementary Data | Consolidated Statements of Operations; Consolidated Statements of Cash Flows; Consolidated Balance Sheets（FY2020–FY2025 财务与现金流）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 5. Market for Registrant’s Common Equity, Related Stockholder Matters and Issuer Purchases of Equity Securities（回购与股息政策/披露）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 8 | Note 15—Stockholders’ Equity（回购与股本相关披露）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 3; Item 8 | Note 20—Legal Matters; Note 5—U.S. and Europe Retrospective Responsibility Plans（重大诉讼与回溯性责任安排）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1A. Risk Factors（监管、竞争、结算赔付义务、网络/系统中断与网络安全等风险）
- SEC EDGAR | Form 10-K | Filed 2024-11-13 | Accession 0001403161-24-000058 | Item 7; Item 8 | Note 1—Summary of Significant Accounting Policies（收入类型、收入确认、client incentives 口径与计量机制）

---

## 公司介绍与沿革

### 结论要点

- Visa 是数字支付领域的全球性参与者之一，通过技术能力在 200+ 国家和地区连接消费者、商户、金融机构与政府等多类主体，服务跨境与本地的商业与资金流动。
- 公司的关键制度与组织沿革可概括为三步：2007 年 10 月完成重组并以 Visa Inc.（特拉华州公司）为核心整合大部分地区实体；2008 年 3 月完成 IPO；2016 年 6 月收购 Visa Europe，实现欧洲业务的公司化整合。
- 【分析】上述里程碑反映了公司从“地区性会员制组织集合”向“统一公司治理与资本市场融资平台”的转变路径；历史上对欧洲的“合同协作→并表整合”变化，是理解其全球一体化与监管暴露面演进的关键线索。

### 详细情况

- 公司定位与业务覆盖
  - Visa 为数字支付服务提供方之一，通过创新技术促成全球商业与资金流动，并在 200+ 国家和地区服务消费者、商户、金融机构与政府等多类参与方。
  - 公司为特拉华州注册主体（Visa Inc.）。

- 组织沿革与关键节点
  - 2007 年 10 月：完成公司重组。重组前，Visa 以多个地区/实体形态运作；重组后，Visa U.S.A.、Visa International、Visa Canada 与 Inovant 等成为 Visa Inc. 的直接或间接子公司；Visa Europe 未成为 Visa Inc. 子公司，仍由其会员金融机构拥有，并在重组中与 Visa Inc. 建立一揽子合同安排；同时发行不同类别/系列股份以反映不同地区会员的权利义务差异。
  - 2008 年 3 月：完成首次公开募股（IPO），为重组后的资本结构与治理框架引入公开市场股权融资机制。
  - 2016 年 6 月 21 日：完成对 Visa Europe 的收购；公司将该交易定位为提升规模、推动整合效率、并受益于 Visa Europe 从会员制向营利性企业转型的关键举措之一。

### 证据与出处

- SEC EDGAR | Form 10-K | Filed 2024-11-13 | Accession 0001403161-24-000058 | Item 1. Business — Overview
- SEC EDGAR | Form 10-K | Filed 2024-11-13 | Accession 0001403161-24-000058 | Cover Page（State or other jurisdiction of incorporation or organization）
- SEC EDGAR | Form 10-K | Filed 2007-12-21 | Accession 0001193125-07-270394 | Item 1. Business — Our Reorganization
- SEC EDGAR | Form 10-K | Filed 2008-11-21 | Accession 0001193125-08-240384 | Item 1. Business — The Reorganization and IPO
- SEC EDGAR | Form 10-K | Filed 2016-11-15 | Accession 0001403161-16-000058 | Item 1. Business — Key Initiatives — Visa Europe Acquisition

---

## 管理层与核心团队

### 结论要点

- 治理结构上，董事会主席与CEO分设：John F. Lundgren为独立董事主席，Ryan McInerney为CEO且兼任董事。
- 核心管理层覆盖关键职能条线：财务、技术、风险与客户服务、人力与企业事务/公司秘书、法务合规；并形成2025财年“named executive officers”口径的核心高管组合。
- 【分析】从履历结构看，核心团队呈“支付/金融+大型科技/工程+风控合规”混合配置，有利于在监管、风控与产品技术迭代三条主线并行推进。

### 详细情况

- 董事会与管理层分工
  - 董事会主席：John F. Lundgren（独立董事；自2024年1月起任董事会主席）。
  - 首席执行官：Ryan McInerney（自2023年2月起任CEO；自2023年2月起任董事）。
  - 董事会对经营的监督方式包括：与关键高管讨论（含CEO、CFO、Vice Chair/公司秘书、总法律顾问、首席风险与客户服务官、技术总裁、首席信息安全官等）、审阅管理层材料，并通过董事会及各委员会的例会机制履职。

- 现任核心高管（含2025财年“named executive officers”相关人员）
  - Ryan McInerney（CEO、董事；年龄50）
    - 任职与背景：自2023年2月起任CEO；曾任Visa President（2013年5月–2023年1月）；此前在JPMorgan Chase与McKinsey & Company任职（含消费者银行与零售银行/支付相关管理岗位）。
  - Chris Suh（Chief Financial Officer；年龄55；2023年7月加入）
    - 职责：负责财务战略、规划与报告，以及财务运营与投资者关系等。
    - 主要经历：曾任Electronic Arts CFO；在Microsoft任多项财务高管职务。
  - Rajat Taneja（President, Technology；年龄61；2013年11月加入）
    - 职责：负责技术创新与投资战略、产品工程、全球IT与运营基础设施，并推动工程与产品团队的整合。
    - 主要经历：曾任Electronic Arts CTO；在Microsoft任Commerce/Online Services等相关高管岗位；为MSCI Inc.董事。
  - Kelly Mahon Tullier（Vice Chair, Chief People and Corporate Affairs Officer, and Corporate Secretary；年龄59；2014年6月加入）
    - 职责：担任公司秘书并负责人力、传播、政府事务、包容性影响与可持续、转型及企业服务等职能（含不动产、航空、安全、全球活动等）。
    - 主要经历：曾任Visa General Counsel（2014年10月–2021年1月）及Chief Legal and Administrative Officer（2021年1月–2021年9月）；此前在PepsiCo等任职。
  - Paul D. Fabara（Chief Risk and Client Services Officer；年龄60；2019年9月加入）
    - 职责：领导全球风险与客户运营职能，负责维护Visa支付系统的完整性与安全，并作为与监管机构的主要联络人；支持反欺诈与安全攻击防护等相关工作。
    - 主要经历：曾在American Express与Barclays等任高级管理岗位。
  - Julie B. Rottenberg（General Counsel；年龄57；2008年2月加入）
    - 职责：负责全球法务、伦理与合规职能，覆盖诉讼、监管、商业协议与并购等事项。
    - 主要经历：曾为Arnold & Porter, LLP合伙人；在Visa曾任北美区域法律负责人等。

- 2025财年“named executive officers”名单（用于高管薪酬披露口径）
  - Ryan McInerney
  - Rajat Taneja
  - Kelly Mahon Tullier
  - Paul D. Fabara
  - Chris Suh

### 证据与出处

- SEC EDGAR | Form DEF 14A | Filed 2025-12-08 | Accession 0001308179-25-000635 | Shareholder Letter（John F. Lundgren为Independent Board Chair；Ryan McInerney为Chief Executive Officer and Director）
- SEC EDGAR | Form DEF 14A | Filed 2025-12-08 | Accession 0001308179-25-000635 | Board and Governance Matters | Director Nominee Biographies（Ryan McInerney任职/年龄/董事任期；John F. Lundgren董事会主席任期等）
- SEC EDGAR | Form DEF 14A | Filed 2025-12-08 | Accession 0001308179-25-000635 | Corporate Governance（董事会监督方式与与关键高管讨论机制）
- SEC EDGAR | Form DEF 14A | Filed 2025-12-08 | Accession 0001308179-25-000635 | Executive Officers（Fabara、Rottenberg、Suh、Taneja、Tullier：职务、年龄、加入时间与履历要点）
- SEC EDGAR | Form DEF 14A | Filed 2025-12-08 | Accession 0001308179-25-000635 | Stock Ownership Information | Directors and Executive Officers（2025财年named executive officers名单）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 10. Directors, Executive Officers and Corporate Governance（Part III信息通过Proxy Statement引用并入）
---

## 公司治理与激励机制

### 结论要点

- 董事会领导结构与独立性：CEO 与董事会主席分设；董事会主席为独立董事；董事候选人中独立董事占比为 91%。
- 董事会关键委员会：设立审计与风险委员会、薪酬委员会、财务委员会、提名与公司治理委员会；各委员会以书面章程为治理基础。
- 高管薪酬与绩效指标（FY2025）：薪酬结构以“可变、与业绩挂钩（at-risk）”为主；年度激励计划的财务目标围绕净收入增长、净利润增长、每股收益增长（“VIP adjusted”口径）。
- 股权激励与归属：股权奖励包含股票期权、RSU、业绩股等；期权与 RSU 通常按三年分期归属；业绩股三年归属并以年度 EPS 目标为核心、叠加相对 TSR（对标 S&P 500）修正；期权行权价与授予日 NYSE 收盘价挂钩。
- 关联交易与追索机制：关联方交易有审计与风险委员会的书面政策与审批框架；设置激励薪酬追索（Clawback/Recoupment）与股权奖励没收条款，覆盖特定情形下的追回与没收。

### 详细情况

- 董事会领导结构与独立性
  - 董事会采用 CEO 与董事会主席分设的领导结构；董事会主席由独立董事担任，并由董事会一致选举产生。
  - 董事候选人中独立董事占比为 91%。
  - 独立董事开展定期的独立董事闭门会议（executive sessions）。

- 董事会关键委员会与职责边界
  - 董事会常设委员会包括：审计与风险委员会、薪酬委员会、财务委员会、提名与公司治理委员会。
  - 各常设委员会均有书面章程；委员会年度工作除按章程履职外，另列示当年关键活动。
  - 审计与风险委员会由独立董事组成，代表董事会监督财务报告流程；管理层对内部财务控制、财务报表编制与对外报告流程承担主要责任。

- 管理层关键岗位（以本章相关信息为限）
  - Ryan McInerney：Chief Executive Officer and Director。
  - John F. Lundgren：Independent Board Chair。

- 高管薪酬构成与绩效指标（FY2025）
  - 目标薪酬结构强调“可变、与业绩挂钩（at-risk）”：CEO 的年度薪酬构成中，目标总直接薪酬里 95% 为可变且 at-risk；其他 NEO 平均为 91%。
  - 年度激励计划（FY2025）财务绩效目标与净收入增长、净利润增长、每股收益增长相关；文件中将对应指标称为 “Net Revenue Growth – VIP adjusted / Net Income Growth – VIP adjusted / EPS Growth – VIP adjusted”。

- 股权激励工具与归属条件
  - 长期激励工具包括股票期权、RSU、业绩股等。
  - 股票期权：按三年分期归属；行权价为授予日 NYSE 收盘价（若授予日为非交易日，则取此前最近一个交易日收盘价）。
  - RSU：按三年分期归属（并存在特定情形下提前全部归属的安排）；归属后可按 1:1 以 A 类普通股或现金（或组合）结算，当前不计划以现金结算；归属期内可获得股息等价物（dividend equivalents）。
  - 业绩股：三年归属；以年度 EPS 目标为基础，并以三年期内相对 TSR（相对 S&P 500 公司）排名作为修正因素。

- 股权激励计划规模与会计处理（与本章相关部分）
  - 2007 Equity Incentive Compensation Plan（经修订与重述）授权薪酬委员会向员工与非雇员董事授予多类股权奖励；授权上限为 198 million 股 A 类普通股（单位：shares）。
  - 股权激励费用确认：授予日计量、扣除预计没收；仅含服务条件的奖励按归属期直线法确认；绩效类奖励按分级归属（graded-vesting）确认，并随绩效期内最佳估计更新。
  - 截至 FY2025 期末，未归属期权对应的未确认补偿成本为 $29 million（单位：USD），预计在约 0.44 年内确认。

- 关联交易与追索机制
  - 关联方交易：审计与风险委员会制定并采用与关联方交易相关的书面政策（Statement of Policy），用于规范关联方交易的审查/批准流程。
  - 薪酬追索（Clawback/Recoupment）：除 Dodd-Frank Act 对激励薪酬追索的强制要求外，Clawback Policy 授权董事会在特定情形下追回更多类型的报酬（包含时间归属型 RSU 与股票期权），适用对象覆盖现任/前任 Executive Committee 成员与 Section 16 officers；股权奖励协议亦包含在特定不利行为情形下的没收条款。

#### 关键术语说明

- NEO(s)
  - 原文引用：For 2025, 95% of the target total direct compensation ... for our Chief Executive Officer was variable and at-risk, and an average of 91% was variable and at-risk for our other NEOs.
  - 中文释义：Named Executive Officers，通常指监管口径下需要在薪酬披露中重点呈现的核心高管群体。

- VIP adjusted
  - 原文引用：In this proxy statement, we refer to these metrics as Net Revenue Growth – VIP adjusted, Net Income Growth – VIP adjusted, and EPS Growth – VIP adjusted.
  - 中文释义：文件对绩效指标口径的命名方式（“VIP adjusted”调整口径）；具体调整项需回到对应章节定义。

- RSU
  - 原文引用：RSUs issued under the EIP primarily vest ratably over three years from the date of grant ...
  - 中文释义：Restricted Stock Units，限制性股票单位；通常在归属后以股票（或现金）结算。

- TSR
  - 原文引用：... a modifier based on Visa’s total shareholder return (TSR) ranking relative to S&P 500 companies ...
  - 中文释义：Total Shareholder Return，总股东回报；此处以相对排名作为业绩股归属的修正因子。

### 证据与出处

- SEC EDGAR | Form DEF 14A | Filed 2025-12-08 | Accession 0001308179-25-000635 | Corporate Governance — Current Leadership Structure（CEO/Chair 分设、独立董事主席、一致选举）
- SEC EDGAR | Form DEF 14A | Filed 2025-12-08 | Accession 0001308179-25-000635 | Independent Oversight（91% independent director nominees；独立董事相关安排）
- SEC EDGAR | Form DEF 14A | Filed 2025-12-08 | Accession 0001308179-25-000635 | Corporate Governance — Committee Composition（审计与风险/薪酬/财务/提名与公司治理委员会；章程）
- SEC EDGAR | Form DEF 14A | Filed 2025-12-08 | Accession 0001308179-25-000635 | Compensation Discussion and Analysis — Variable over Fixed Pay（95%/91% variable and at-risk）
- SEC EDGAR | Form DEF 14A | Filed 2025-12-08 | Accession 0001308179-25-000635 | Compensation Discussion and Analysis — Fiscal Year 2025 Compensation — Select Corporate Performance Goals and Results for Fiscal Year 2025（年度激励计划指标与 VIP adjusted 口径）
- SEC EDGAR | Form DEF 14A | Filed 2025-12-08 | Accession 0001308179-25-000635 | Compensation Discussion and Analysis — Performance Shares / Stock Options / Restricted Stock Units（归属周期、EPS+相对TSR、期权行权价政策）
- SEC EDGAR | Form DEF 14A | Filed 2025-12-08 | Accession 0001308179-25-000635 | Certain Relationships and Related Person Transactions（关联方交易政策与流程）
- SEC EDGAR | Form DEF 14A | Filed 2025-12-08 | Accession 0001308179-25-000635 | Other Policies and Practices — Recoupment Policies（Clawback/Recoupment、适用对象与触发条件）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 8. Financial Statements and Supplementary Data — Note 17—Share-based Compensation — Equity Incentive Compensation Plan（2007 EIP、198 million shares 授权）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 8. Financial Statements and Supplementary Data — Note 17—Share-based Compensation（RSU 归属与结算；费用确认；未确认补偿成本）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Report of Independent Registered Public Accounting Firm（审计师：KPMG LLP）

## 股权结构、投票权和主要股东

### 结论要点

- 公司普通股包含 Class A、Class B-1、Class B-2、Class C；Class A 在纽约证券交易所交易（代码：V），Class B-1、B-2、Class C 目前不存在公开交易市场。
- 截至 2025-10-30，公司披露普通股在外流通股数为：Class A 1,687,629,770 股；Class B-1 4,835,384 股；Class B-2 120,338,948 股；Class C 8,938,707 股。
- Class B-1、B-2、Class C 普通股与 Series A/B/C 优先股存在“有限投票权”与在满足条件时向 Class A 转换的安排；相关转换可能改变 Class A 的在外股数与投票权分布。
- DEF 14A 口径下，超过 5% 的 Class A 普通股受益所有人包括 The Vanguard Group（8.18%）与 BlackRock Inc.（7.32%）；同一口径下董事与高管个人持股均未超过 Class A 在外股数的 1%。

### 详细情况

- 股权类别与交易市场
  - Class A 普通股在纽约证券交易所交易，交易代码为 V。
  - Class B-1、Class B-2、Class C 普通股目前不存在公开交易市场。
  - 截至 2025-10-30，公司披露普通股在外流通股数为：Class A 1,687,629,770 股；Class B-1 4,835,384 股；Class B-2 120,338,948 股；Class C 8,938,707 股。

- 投票权与转换安排（多类别普通股与优先股）
  - Class B-1、Class B-2、Class C 普通股持有人投票权为“有限投票权”，但在若干重大交易上可参与表决，包括拟议的合并/并购、退出核心支付业务，以及特拉华州公司法要求的其他表决事项。
  - Series A/B/C 优先股在特定合并/并购情形下具有有限表决权，典型情形包括：优先股持有人将获得与该系列优先股在偏好、权利与特权方面不实质相同的股权证券；或（就 Series B/C 而言）优先股持有人将获得与 Class A 普通股股东不同的证券、现金或其他财产对价。
  - 在诉讼相关的安排下，Class B-1 与 Class B-2 普通股在“美国 covered litigation 最终解决”后将变得可转换为 Class A 普通股；同时，Series B 与 Series C 优先股在分阶段释放安排下，最迟不晚于 2028 年将完全可转换为 Series A 优先股或 Class A 普通股（并受用于覆盖未决索赔的留存安排影响）。
  - 【分析】若发生上述转换，Class A 在外股数将增加，从机制上稀释既有 Class A 普通股股东的投票权；若转换后的 Class A 大规模进入二级市场，也可能对 Class A 股价形成压力（方向性取决于转换规模、出售节奏与市场承接）。

- 主要股东（Class A，DEF 14A 口径）
  - DEF 14A 以 2025-12-01 的 Class A 在外股数 1,685,772,208 股为基准，列示超过 5% 的 Class A 普通股受益所有人包括：
    - The Vanguard Group：141,408,295 股，占 Class A 的 8.18%（其 Schedule 13G/A 披露日期为 2024-02-13）。
    - BlackRock Inc.：126,566,875 股，占 Class A 的 7.32%（其 Schedule 13G/A 披露日期为 2024-02-08）。
  - 同一口径下，董事与“named executive officers”个人持股均未超过 1%（并同时给出可在 60 日内取得的股份口径与合计口径）。

- 同一指标的口径差异（在外股数）
  - 10-K 披露截至 2025-10-30 的 Class A 在外股数为 1,687,629,770 股；DEF 14A 披露截至 2025-12-01 的 Class A 在外股数为 1,685,772,208 股。
  - 上述差异对应不同截至日期与披露口径；以各自披露日期口径为准。

### 证据与出处

- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Cover Page（Title of each class / Trading symbol / Exchange）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 5 | Market for Registrant’s Common Equity, Related Stockholder Matters and Issuer Purchases of Equity Securities（B-1/B-2/C 无公开交易市场；截至 2025-10-30 各类普通股在外股数）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1A | Risk Factors（Class B-1/B-2/C 与 Series A/B/C 投票权与转换安排；“Holders of our class B-1, B-2 and C common stock and series A, B and C preferred stock may have different interests …”相关风险段落）
- SEC EDGAR | Form DEF 14A | Filed 2025-12-08 | Accession 0001308179-25-000635 | Stock Ownership Information | Beneficial Ownership of Equity Securities（Class A 在外股数基准日；董事与高管持股口径）
- SEC EDGAR | Form DEF 14A | Filed 2025-12-08 | Accession 0001308179-25-000635 | Stock Ownership Information | Principal Shareholders Class A Common Stock（超过 5% 的 Class A 受益所有人及持股比例）

---

## 股本变化历史及主要原因

### 结论要点

- FY2020–FY2023：Class A 普通股期末流通股分别为 1,683,000,000、1,677,000,000、1,635,000,000、1,594,000,000 股。
- 【分析】FY2020–FY2023 存在持续的公开市场回购并注销（分别回购 44、40、56、55 百万股），与 Class A 期末流通股的下降方向一致。
- FY2024：股本结构出现一次性调整，Class B 按公司章程修订更新为 Class B-1/Class B-2，并在交换要约后 B 类期末流通股由 245,000,000 降至 125,000,000 股；同期 Class A 期末流通股为 1,733,000,000 股。
- FY2025：Class A 期末流通股为 1,691,000,000 股；公开市场回购 54 百万股（总成本 18,185 百万美元），回购股已注销并构成“authorized but unissued shares”。

### 详细情况

- 口径说明：以下 FY 均为公司财年口径，财年截至日为每年 9 月 30 日；表内为各类普通股截至财年末（9/30）的期末流通股（shares outstanding）。
- 各财年期末普通股流通股（按类别）：
  | FY（截至9/30） | Class A 普通股期末流通股 | Class B / B-1 / B-2 期末流通股 | Class C 普通股期末流通股 |
  | --- | ---: | ---: | ---: |
  | FY2020 | 1,683,000,000 | Class B：245,000,000 | 11,000,000 |
  | FY2021 | 1,677,000,000 | Class B：245,000,000 | 10,000,000 |
  | FY2022 | 1,635,000,000 | Class B：245,000,000 | 10,000,000 |
  | FY2023 | 1,594,000,000 | Class B：245,000,000 | 10,000,000 |
  | FY2024 | 1,733,000,000 | Class B-1：5,000,000；Class B-2：120,000,000（合计 125,000,000） | 10,000,000 |
  | FY2025 | 1,691,000,000 | Class B-1：5,000,000；Class B-2：120,000,000（合计 125,000,000） | 9,000,000 |
- 公开市场回购（Open market repurchases，按披露表格原单位：shares 为“百万股”，金额为“百万美元”）：
  - FY2020–FY2022：分别回购 44、40、56；平均回购价分别为 $183.00、$219.03、$206.47；总成本分别为 8,114、8,676、11,589。
  - FY2023–FY2025：分别回购 55、64、54；平均回购成本分别为 $222.27、$266.24、$335.44；总成本分别为 12,182、16,958、18,185。
- FY2024 的 Class B 结构调整与交换要约（exchange offer）要点：
  - 2024-01-23：普通股股东批准对公司章程的修订，授权实施 exchange offer program，以允许持有人用部分 Class B 普通股交换为可自由交易的 Class C 普通股；该等修订同时将修订日所有在外流通的 Class B 普通股自动“redenominated”为 Class B-1 普通股（权利与特征不变），并授权在 exchange offer 中发行新的 Class B 类别。
  - 2024-05-06：公司在交换要约中接受 241 百万股 Class B-1 普通股的 tender；2024-05-08：发行约 120 百万股 Class B-2 普通股及 48 百万股 Class C 普通股；被交换的 Class B-1 普通股已注销并构成“authorized but unissued shares”。
- FY2025 最新披露日（latest practicable date）在外流通普通股（按类别，shares outstanding）：截至 2025-10-30，Class A 为 1,687,629,770 股；Class B-1 为 4,835,384 股；Class B-2 为 120,338,948 股；Class C 为 8,938,707 股。

### 证据与出处

- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 8 | Note 15—Stockholders’ Equity（各类普通股期末流通股、公开市场回购表、回购注销口径、latest practicable date 各类普通股在外流通股数）
- SEC EDGAR | Form 10-K | Filed 2024-11-13 | Accession 0001403161-24-000058 | Item 8 | Note 15—Stockholders’ Equity（Class B 章程修订与 exchange offer、B-1/B-2/C 股数与变化、B-1 tender 后注销与 B-2/C 发行）
- SEC EDGAR | Form 10-K | Filed 2023-11-15 | Accession 0001403161-23-000099 | Item 8 | Note 15—Stockholders’ Equity（FY2023/FY2022 各类普通股期末流通股）
- SEC EDGAR | Form 10-K | Filed 2022-11-16 | Accession 0001403161-22-000081 | Item 8 | Note 15—Stockholders’ Equity（FY2022/FY2021 各类普通股期末流通股、FY2022–FY2020 公开市场回购表与回购注销口径）
- SEC EDGAR | Form 10-K | Filed 2021-11-18 | Accession 0001403161-21-000060 | Item 8 | Note 15—Stockholders’ Equity（FY2021/FY2020 各类普通股期末流通股）
- SEC EDGAR | Form 10-K | Filed 2020-11-19 | Accession 0001403161-20-000070 | Item 8 | Note 15—Stockholders’ Equity（FY2020/FY2019 各类普通股期末流通股）

---

## 股东回报

### 结论要点

- FY2020–FY2025 持续同时进行现金分红与回购；季度现金股息（每股）由 FY2020 的 $0.30 提升至 FY2025 的 $0.59。
- 回购为主要回报方式：FY2020–FY2025 回购现金支出为 8,114,000,000–18,316,000,000 美元，高于同期现金股息支付额 2,664,000,000–4,634,000,000 美元。
- FY2025 截至 2025-09-30，股份回购项目剩余额度为 $24.9 billion（remaining authorized funds）。

### 详细情况

#### 股东回报历史

- FY2025
  - 股息动作：季度现金股息（每股）$0.59；季度股息加总（每股）$2.36（$0.59×4）；现金股息支付额 4,634,000,000 美元。
  - 回购动作：回购现金支出 18,316,000,000 美元；回购并注销 54,000,000 股，成本 18,185,000,000 美元。

- FY2024
  - 年度股息：现金股息支付额 4,217,000,000 美元。
  - 季度股息加总：季度现金股息（每股）$0.52；季度股息加总（每股）$2.08（$0.52×4）。
  - 回购：回购现金支出 16,713,000,000 美元；回购并注销 64,000,000 股，成本 16,958,000,000 美元。

- FY2023
  - 年度股息：现金股息支付额 3,751,000,000 美元。
  - 季度股息加总：季度现金股息（每股）$0.45；季度股息加总（每股）$1.80（$0.45×4）。
  - 回购：回购现金支出 12,101,000,000 美元；回购并注销 55,000,000 股，成本 12,182,000,000 美元。

- FY2022
  - 年度股息：现金股息支付额 3,203,000,000 美元。
  - 季度股息加总：季度现金股息（每股）$0.375；季度股息加总（每股）$1.50（$0.375×4）。
  - 回购：回购现金支出 11,589,000,000 美元；回购并注销 56,000,000 股，成本 11,589,000,000 美元。

- FY2021
  - 年度股息：现金股息支付额 2,798,000,000 美元。
  - 季度股息加总：季度现金股息（每股）$0.32；季度股息加总（每股）$1.28（$0.32×4）。
  - 回购：回购现金支出 8,676,000,000 美元；回购并注销 40,000,000 股，成本 8,676,000,000 美元。

- FY2020
  - 年度股息：现金股息支付额 2,664,000,000 美元。
  - 季度股息加总：季度现金股息（每股）$0.30；季度股息加总（每股）$1.20（$0.30×4）。
  - 回购：回购现金支出 8,114,000,000 美元；回购并注销 44,000,000 股，成本 8,114,000,000 美元。

#### 最新股东回报政策

- 【前瞻（原文）】We expect to continue paying quarterly dividends in cash, subject to approval by the board of directors.
- 【前瞻（原文）】The declaration and payment of future dividends is at the sole discretion of our board of directors after taking into account various factors, including our financial condition, settlement indemnifications, operating results, available cash and current and anticipated cash needs.
- 回购计划：FY2025 回购 54 million shares for $18.2 billion；截至 2025-09-30，回购项目 remaining authorized funds 为 $24.9 billion。

### 证据与出处

- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Cover Page（Fiscal year ended September 30, 2025）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 5. Market for Registrant’s Common Equity, Related Stockholder Matters and Issuer Purchases of Equity Securities
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Financial Statements—Consolidated Statements of Cash Flows
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Note 15—Stockholders’ Equity
- SEC EDGAR | Form 10-K | Filed 2024-11-13 | Accession 0001403161-24-000058 | Financial Statements—Consolidated Statements of Cash Flows
- SEC EDGAR | Form 10-K | Filed 2024-11-13 | Accession 0001403161-24-000058 | Note 15—Stockholders’ Equity
- SEC EDGAR | Form 10-K | Filed 2022-11-16 | Accession 0001403161-22-000081 | Financial Statements—Consolidated Statements of Cash Flows
- SEC EDGAR | Form 10-K | Filed 2022-11-16 | Accession 0001403161-22-000081 | Note 15—Stockholders’ Equity
---

## 产品与服务及护城河

### 结论要点

- 【分析】产品与服务按三条主线组织：消费支付（CP）、商业与资金流动解决方案（CMS，含 Visa Direct 等）、增值服务（VAS）；底层以 VisaNet 与“network of networks”提供资金流动与交易处理的统一连接能力。
- 【分析】护城河主要来自双边网络效应与规模（支付凭证、商户受理覆盖、跨境与多网络连接）以及安全与风控能力（代币化、风险管理与反欺诈），并通过模块化能力与集成方式提升客户粘性。
- 截至 2025-09-30：支付凭证近 50 亿、覆盖超 1.75 亿商户受理点；基础层可连接约 120 亿张卡/银行账户/数字钱包；提供 200+ 项产品与服务；VTS 已 provisioned 160 亿 tokens；Visa Direct 潜在触达约 120 亿端点，2025 财年处理超过 125 亿笔交易。

### 详细情况

#### 产品与服务框架（CP / CMS / VAS）

- 消费支付（CP）
  - 覆盖信用卡、借记卡、预付卡与现金取款等 Visa 品牌支付产品；典型交易链路围绕授权、清算与结算展开，连接消费者、发卡机构、收单机构与商户的“四方模式”。
  - 近场与数字化能力示例：Tap to Phone 在 2025 财年累计超过 2,000 万台发生交易的设备；Tap to Add Card 覆盖超过 600 家发卡机构并在全球超过 14 亿张 Visa 信用与借记卡上线；2025 年推出 Visa Pay，用于把参与的数字钱包通过数字化凭证接入全球受理网络。

- 商业与资金流动解决方案（CMS）
  - 覆盖 C2B 之外的资金流动与支付场景（P2P、B2C、B2B、G2C 等），并通过多网络连接增强本地与跨境能力。
  - Visa Direct：面向国内与跨境资金流动，覆盖 P2P、A2A 转账、企业与政府向个人/小微的付款、商户结算与退款等；覆盖超过 195 个国家与地区；使用超过 90 个国内支付体系与超过 60 个卡与钱包网络，潜在触达约 120 亿端点；2025 财年处理超过 125 亿笔交易、服务超过 650 个合作伙伴。

- 增值服务（VAS）
  - 服务族群包括 Issuing Solutions、Acceptance Solutions、Risk and Security Solutions、Advisory and Other Services；既可与支付网络服务打包提供，也可作为独立产品以固定或按交易计费方式提供。

#### 产品组合的底层架构与交付方式

- Visa as a Service（四层栈）
  - 基础层：网络基础设施连接约 120 亿张卡/银行账户/数字钱包，并覆盖超过 1.75 亿商户受理点、跨越 200+ 个国家与地区。
  - 服务层：把认证、风险管理与欺诈检测等能力组件化，支持复用与组合。
  - 解决方案层与接入层：在组件化能力之上组合形成面向不同客户/场景的解决方案，并通过 API、MCP server 等方式提供接入。

#### 护城河拆解（与可核查事实对齐）

- 【分析】规模与网络效应
  - 近 14,500 家金融机构使用其产品与服务体系构建面向个人、企业与政府的支付解决方案；支付凭证规模与商户受理覆盖形成正反馈，有利于提升网络对新客户与新场景的吸引力。
- 【分析】多网络连接能力（network of networks）
  - 在“单一连接点”之上扩展到多端点（卡、银行账户、数字钱包等）与多网络（国内支付体系、卡与钱包网络），使资金流动能力可在不同场景复用并加速新用例落地。
- 【分析】安全、风控与信任
  - 代币化用于保护数字交易信息并降低风险；VTS 以 token 替代 16 位账户号并结合加密信息等机制，形成面向线上线下多场景的安全能力底座；安全与风控能力与受理网络规模共同强化对发卡行、收单方、商户与消费者的粘性。
- 【分析】产品与能力的“组件化”带来的迁移成本
  - 以组件化能力与 API 接入为主的交付方式，使客户在认证、风控、受理与资金流动等多个环节形成能力耦合；更换或拆分需要同步替代多项能力与集成路径，提升迁移门槛。

#### 关键术语说明

- VisaNet
  - 原文引用：“We are focused on extending, enhancing and investing in our proprietary advanced transaction processing network, VisaNet…”
  - 中文释义：公司的自有交易处理网络，用于支持授权、清算与结算等核心处理能力，并作为连接多类端点与多网络的基础设施。
- Visa Token Service（VTS）
  - 原文引用：“VTS helps protect digital transactions by replacing 16-digit Visa account numbers with a token… As of September 30, 2025, Visa has provisioned more than 16 billion tokens.”
  - 中文释义：代币化服务，用 token（替代账号并叠加加密信息等）保护数字交易数据；截至 2025-09-30 已发行（provisioned）160 亿以上 tokens。
- Visa Direct
  - 原文引用：“Visa Direct… with the potential to reach approximately 12 billion endpoints… In fiscal 2025, Visa Direct processed more than 12.5 billion transactions…”
  - 中文释义：资金流动平台，覆盖国内与跨境多类转账/付款场景，连接卡、银行账户与数字钱包等端点；2025 财年处理超过 125 亿笔交易。

### 证据与出处

- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1. Business（Overview；Our Core Business/four-party model；Visa as a Service stack；Strategy：CP/CMS/VAS；Consumer Payments；Commercial and Money Movement Solutions；Visa Direct；Token technology / Visa Token Service）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 8. Financial Statements and Supplementary Data（Notes：Revenue Recognition / Value-added Services）

## 关键第三方依赖

### 结论要点

- 业务链条对外部参与方的依赖主要体现在支付网络生态：交易处理发生在消费者、发卡与收单金融机构及商户之间；账户持有人与商户关系多数由金融机构客户管理。
- 网络安全治理将第三方（服务提供商、供应商等）纳入同一风险管理框架，包含准入尽调与合同审计权等安排；同时存在框架执行与覆盖不足的风险情景。
- 客户履约相关的结算安排包含客户保证金（受限）等机制，可能影响可动用资金结构但在会计上与对应负债抵销列示。

### 详细情况

#### 关键依赖项清单（云/平台分发/数据或内容授权/支付/关键外包与SaaS等）

- 支付网络生态参与方：公司提供交易处理服务（主要包括授权、清算与结算），交易在消费者、发卡与收单金融机构及商户之间通过其电子支付网络完成；公司本身不发卡、不放贷，也不为持卡人设定费率与费用，多数情况下持卡人与商户关系由金融机构客户拥有并管理。
- 第三方网络安全相关依赖：网络安全风险管理覆盖服务提供商、供应商等第三方，并将第三方关系相关网络安全风险纳入统一管理框架。
- 结算履约相关安排：为确保部分客户在支付服务项下的结算义务履行，公司持有来自部分客户的现金保证金及其他非现金资产；现金保证金作为受限资产并与对应负债抵销列示。

#### 集中度、替代性与议价权（按披露与可核查信息）

- 客户集中度：在截至 2023-09-30、2024-09-30、2025-09-30 的财年口径下，单一主要客户对应的净收入集中度指标为 11%。
- 【分析】支付网络型业务通常依赖多边参与方协同（发卡行、收单机构、商户等），关键环节的合作关系与规则变动可能通过受理覆盖、交易量与服务落地节奏传导至经营表现；该影响强度取决于合作方结构与具体合同/规则安排。

#### 成本与条款对毛利/现金流的影响

- 客户保证金：现金保证金为受限资产、不能用于一般经营活动，并与对应负债抵销列示；相关安排的规模变化可能改变现金类资产结构与结算相关负债结构。

#### 依赖风险与缓释安排

- 第三方网络安全风险管理机制：对服务提供商、供应商等第三方执行准入尽调，并在合同中设置审计权，用于识别与第三方关系相关的网络安全风险，风险评估与管理深度与第三方提供产品/服务的固有风险及其可接触的信息与技术资产敏感度相匹配。
- 【前瞻（原文）】“our third-party risk management framework may not be implemented effectively or may not be successful or sufficient to mitigate all of our risks.”
- 已知事件口径：截至 2025-09-30，过去三个财年内未出现公司已知的、对业务战略、经营结果或财务状况产生重大影响的直接或第三方网络安全事件。
- 并购资产的差异化控制：对部分并购形成且未完全纳入标准技术平台或未托管于数据中心的实体，设置与其规模与运营相匹配、但仍基于同类国际标准的单独控制要求，并向管理层与董事会进行定期汇报。

### 证据与出处

- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1C. Cybersecurity（第三方风险管理：尽调、审计权、框架可能不足；已知网络安全事件口径；并购实体差异化控制与汇报）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 8. Financial Statements and Supplementary Data | Note 1—Summary of Significant Accounting Policies（Organization；Customer collateral）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 8. Financial Statements and Supplementary Data | XBRL（Major customers / Concentration risk：us-gaap:ConcentrationRiskPercentage1；MajorCustomersAxis=v:CustomerOneMember；CustomerConcentrationRiskMember；SalesRevenueNetMember；contexts c-301/c-303/c-302）
---

## 获客与分发渠道（直销/平台/合作伙伴）

### 结论要点

- 分发路径以金融机构客户为核心：支付网络服务直接交付给发卡机构（issuer）与收单机构（acquirer），再由其触达商户与消费者；多数情况下，持卡人与商户关系由金融机构客户管理。
- 商户侧拓展与定价职责主要在收单侧：收单机构负责向商户收取 MDR 并进行商户拓展；interchange reimbursement fees 一般由收单方向发卡方支付，Visa 设定在缺少其他结算条款时适用的默认 interchange reimbursement fees，并强调该默认费率与其从发卡/收单收取的收入相互独立。
- 合作条款中存在面向金融机构客户、商户及其他业务伙伴的长期激励合同；激励在会计呈现上通常作为净收入抵减（client incentives），并形成对应的 client incentives 资产/负债的跨期确认与计量。
- 【分析】渠道可概括为 B2B2X：与 issuer/acquirer 的商业条款（费率结构、激励合同、结算与担保安排）决定网络服务对商户受理与支付量的传导效率。

### 详细情况

#### 渠道结构与分发路径（直销/平台/合作伙伴/应用商店/广告投放等）

- VisaNet 提供交易处理服务，覆盖授权（authorization）、清算（clearing）与结算（settlement）等环节。
- 支付网络服务直接交付给 issuer 与 acquirer，后者向支付网络内的商户与消费者提供相关服务；净收入主要来自 issuer 与 acquirer。
- 多数情况下，持卡人与商户关系由金融机构客户管理。
- interchange reimbursement fees 一般由收单方向发卡方支付；收单机构负责向商户收取 MDR 并进行商户拓展；Visa 设定在缺少其他结算条款时适用的默认 interchange reimbursement fees，并强调该默认费率与其从 issuer/acquirer 收取的收入相互独立。

#### 关键合作条款

- 长期合同对象包括金融机构客户、商户及其他业务伙伴；激励目的包括提升支付量、提升 Visa 产品受理、促进商户受理与使用 Visa 支付服务、推动创新。
- 激励通常计入净收入抵减（client incentives）；若现金支付用于交换客户提供的独立商品或服务，则计入经营费用（operating expenses）。
- upfront 与固定激励支付在支付时通常确认为 client incentives 资产，并在合同期内按直线法作为净收入抵减进行摊销。
- 基于绩效目标（performance targets）赚取的激励在赚取时作为净收入抵减确认，未支付部分确认为 client incentives 负债；相关估计会随绩效预期、实际表现、合同修订或新签合同而调整。
- client incentives 资产与负债按 12 个月经营周期划分为流动或非流动。

#### 结算与回款

- 美元与金融机构客户的多数结算在同日完成，通常不形成应收/应付；非美元结算一般会有一到两个工作日的在途期，从而形成 settlement receivable 与 settlement payable，并在资产负债表列示。
- 为确保客户按 operating rules 履行结算义务，Visa 从部分客户收取现金押品及其他非现金资产；现金押品作为受限资产，并与对应负债完全抵销列示。
- 对因其他客户未按 operating rules 履行结算义务导致的结算损失，Visa 向金融机构客户提供 settlement losses 的赔付安排（settlement indemnification）；相关担保/赔付义务在满足确认条件时于初始时点确认，并对预计信用损失计提 allowance；该负债的估计公允价值计入 accrued liabilities。
- 【占位符】
  - 缺口：本章所需的“获客组织形态/区域直销覆盖/渠道费用结构/具体分成或费率表/排他条款/接口与数据共享的商业条款/回款与应收账款管理（坏账政策、账期等）”的可核查细节。
  - 需要：10-K 中对销售与客户拓展、合作条款（含费率/分成/投放/排他/接口商业条款）、应收账款与坏账政策的明确段落与章节标题定位。
  - 已检索范围：SEC 10-K（2024-11-13，0001403161-24-000058）中的 Item 1. Business（渠道职责与费率边界相关段落）及财务报表附注 Note 1（收入确认、client incentives、结算应收应付、客户押品、担保与赔付安排）。
  - 下一步：在同一份 10-K 内进一步定位并补齐销售/客户拓展与应收账款坏账政策等章节；若仍无法定位到明确表述，则以最终监管披露为准。

#### 关键术语说明

- Issuer / Acquirer
  - 原文引用：The Company delivers its payments network services directly to issuers and acquirers, who provide those services to others within the payments network: the merchants and consumers.
  - 中文释义：issuer 指发卡机构；acquirer 指收单机构。Visa 的直接“客户/对价方”主要为 issuer 与 acquirer，商户与消费者主要通过收单/发卡体系触达与服务。
- MDR
  - 原文引用：Our acquiring clients are responsible for setting the fees they charge to merchants for the MDR and for soliciting merchants.
  - 中文释义：MDR（merchant discount rate）为收单机构向商户收取的费用（概念层面的费率/收费项）；商户拓展与商户侧收费由收单机构负责。
- Client incentives
  - 原文引用：The Company enters into long-term contracts with financial institution clients, merchants and other business partners for various programs that provide cash and other incentives designed to increase revenue by growing payments volume, increasing Visa product acceptance, encouraging merchant acceptance and use of Visa payment services and driving innovation.
  - 中文释义：client incentives 为面向客户/合作伙伴的现金或其他激励安排；在会计上通常作为净收入的抵减项目，并可能形成跨期的激励资产/负债。
- Settlement receivable and payable
  - 原文引用：Most U.S. dollar settlements with the Company’s financial institution clients are settled within the same day and do not result in a receivable or payable balance. Settlements in currencies other than the U.S. dollar generally remain outstanding for one to two business days, resulting in amounts due from and to clients.
  - 中文释义：结算应收/应付反映清算结算在途产生的短期资金往来；美元多数同日结算，非美元结算在途期更长，从而更可能形成应收/应付。

### 证据与出处

- SEC EDGAR | Form 10-K | Filed 2024-11-13 | Accession 0001403161-24-000058 | Note 1—Summary of Significant Accounting Policies | Organization（VisaNet；authorization/clearing/settlement；持卡人与商户关系归属金融机构客户）
- SEC EDGAR | Form 10-K | Filed 2024-11-13 | Accession 0001403161-24-000058 | Note 1—Summary of Significant Accounting Policies | Revenue recognition（直接交付给 issuers/acquirers；merchant/consumer 的分发路径；净收入主要来自 issuers/acquirers）
- SEC EDGAR | Form 10-K | Filed 2024-11-13 | Accession 0001403161-24-000058 | Item 1. Business（interchange reimbursement fees；默认费率适用条件；MDR 由收单机构向商户收取并负责商户拓展；Visa 向收单收取费用与 MDR 独立）
- SEC EDGAR | Form 10-K | Filed 2024-11-13 | Accession 0001403161-24-000058 | Note 1—Summary of Significant Accounting Policies | Client incentives（长期合同对象与目的；净收入抵减与费用分类；client incentives 资产/负债的确认与计量）
- SEC EDGAR | Form 10-K | Filed 2024-11-13 | Accession 0001403161-24-000058 | Note 1—Summary of Significant Accounting Policies | Settlement receivable and payable（结算在途期与应收/应付形成）
- SEC EDGAR | Form 10-K | Filed 2024-11-13 | Accession 0001403161-24-000058 | Note 1—Summary of Significant Accounting Policies | Customer collateral（押品目的；operating rules；现金押品受限且与负债抵销列示）
- SEC EDGAR | Form 10-K | Filed 2024-11-13 | Accession 0001403161-24-000058 | Note 1—Summary of Significant Accounting Policies | Guarantees and indemnifications（settlement losses 赔付安排；operating rules；预计信用损失与 allowance；负债列示口径）

## 用户与客户发展

### 结论要点

- 客户生态以金融机构客户与商户侧为核心；FY2025披露：近14,500 家金融机构客户、近 5 billion 支付凭证（payment credentials）、覆盖全球超 175 million 商户受理点；Visa 的 total payments and cash volume 为 $17 trillion。
- 客户/地域集中度：净收入按地域主要基于发卡行或收单行所在地区；FY2025/2024/2023 美国净收入占比分别约 39%/41%/43%，除美国外无单一国家达到总净收入的 10%；FY2025/2024/2023 各期均有单一客户贡献 11% 总净收入。
- 【分析】在净收入集中度披露与“客户可调整承诺/在特定情形下可较短通知期终止合作”的风险披露背景下，大客户关系稳定性与合作条款变化对经营波动的影响权重较高。

### 详细情况

#### 客户结构与集中度（行业/地域/前N大客户占比）

- 客户结构（经营生态）：公司披露其交易处理服务（授权、清算与结算）连接消费者、发卡金融机构、收单金融机构与商户（sellers）的“四方模型”；并披露其 Visa-branded payment products 被近 14,500 家金融机构客户用于向个人/企业/政府账户持有人提供信用卡、借记卡、预付卡与现金提取等方案。
- 规模与覆盖（FY2025）：公司披露 FY2025 total payments and cash volume 为 $17 trillion；披露其近 5 billion payment credentials（issued Visa card accounts）可在全球超 175 million merchant locations 使用。
- 地域集中度（净收入口径）：公司披露净收入按地域主要基于发卡或收单金融机构所在地；FY2025/2024/2023 美国净收入占总净收入约 39%/41%/43%，除美国外无单一国家在上述年度达到总净收入的 10%。
- 客户集中度（净收入口径）：公司披露 FY2025/2024/2023 各期均有单一客户贡献其总净收入的 11%。

#### 留存与扩张（DAU/MAU、年度活跃买家、续费率、NRR、流失原因——以披露为准）

- 客户关系稳定性相关披露：公司在风险披露中指出，其金融机构客户与商户侧客户可随时重新评估对公司的承诺或发展自有竞争性服务；并指出部分客户通常具有发行非 Visa 产品的灵活性，且在特定情形下金融机构客户可能在较短通知期终止合同关系且无需支付显著提前解约费用。
- 【占位符】
  - 缺口：DAU/MAU、NRR、续费率、流失原因等“留存/扩张”类KPI的定义口径与时间序列披露。
  - 需要：公司在监管披露/财报中对上述指标的明确定义、披露期与历史序列（如有）。
  - 已检索范围：SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1. Business；Item 1A. Risk Factors；Item 8（Note 1、Note 12、Note 14）。
  - 下一步：在后续 10-Q/10-K 与公司投资者材料中持续检索同口径指标披露；如出现披露则按原文补齐并与经营指标章节联动。

#### 回款与信用质量（DSO、应收变化、坏账计提口径）

- 结算担保与信用风险：公司披露其对金融机构客户提供结算担保（settlement risk guarantee），在客户未按 Visa operating rules 履行结算义务时对其结算损失予以赔付；该安排使公司面临由“交易发生日至后续结算日”的时点差异带来的结算风险，并披露其通过全球结算风险政策与流程管理结算风险，可能要求客户在不满足特定信用标准时提交抵押品（collateral）。
- 结算敞口与抵押品规模：公司披露 FY2025 最大单日结算敞口为 $153.4 billion、平均单日结算敞口为 $91.2 billion；并披露截至 2025-09-30 与 2024-09-30 的抵押品总额分别为 $8.8 billion 与 $7.7 billion。
- 预期信用损失与客户抵押品的会计呈现：公司披露其对结算担保义务估计并确认预期信用损失（expected credit losses）的准备；并披露其从部分客户取得现金存款及其他非现金资产作为客户抵押品以保障结算义务履行，其中现金抵押品资产为受限（restricted）并由相应负债全额对冲列示于资产负债表。

### 证据与出处

- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1. Business | Our Core Business（金融机构客户数量、payments and cash volume、payment credentials、merchant locations等经营规模披露）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1A. Risk Factors | Our revenue and profits are dependent on our client and seller base（客户可调整承诺/终止合作、集中度相关风险表述）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 8. Financial Statements and Supplementary Data | Note 14—Segment Information（净收入地域口径、美国占比、单一客户占比等集中度披露）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 8. Financial Statements and Supplementary Data | Note 12—Settlement Guarantee Management（结算担保机制、FY2025结算敞口、抵押品规模披露）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 8. Financial Statements and Supplementary Data | Note 1—Summary of Significant Accounting Policies（expected credit losses 与客户抵押品列报口径披露）

## 未来产品规划与商业规划

### 结论要点

- 产品与商业规划呈现“能力组件化 + 网络化交付”特征：线下接触式（Tap）→ 账户与设备安全（token）→ A2A/开放银行触达 → 国内与跨境资金流动（Visa Direct/Visa+）→ 增值服务（VAS）组合推进。
- 线下接触式侧，FY2025 线下面对面交易中 Tap to Pay 占比为全球 79%、美国 66%；同时围绕 Tap to Phone、Tap to Add Card、Tap to Confirm 等“Tap”能力扩展更多场景。
- 安全与 token 能力侧，Visa Token Service（VTS）以 token 替代 16 位账号用于多场景交易；截至 2025-09-30 已 provisioned 超过 160 亿 tokens，并延伸到云端 token 框架与 passkey 绑定能力。
- 消费者支付与 A2A 侧，通过 Visa Pay（2025）连接数字钱包/方案/银行至 Visa 网络，同时借助 Tink 扩展 open banking payments network 至 “thousands of bank connections”（截至 2025-09-30）。
- 资金流动侧，Visa Direct 覆盖国内与跨境资金划转与多用例支付/结算；FY2025 处理交易超过 125 亿笔、合作伙伴超过 650 家；同时提出 Visa+ 的别名凭证（alias credential）路径（属于前瞻性表述）。
- 监管侧风险披露指出，tokenization、push payments、cross-border money movement 等新能力“could bring increased licensing or authorization requirements”，产品扩张与资质/合规要求同步抬升。

### 详细情况

#### 线下接触式与“Tap”能力扩展

- FY2025 线下面对面交易中，Tap to Pay 占比为全球 79%、美国 66%。
- FY2025 全球公共交通场景：已激活超过 1,000 个 contactless public transport projects；在全球交通系统上处理的 contactless transactions 超过 24 亿笔。
- FY2025 Tap to Phone：Tap to Phone transacting devices 超过 2,000 万台。
- Tap to Add Card：于 2024 年推出；超过 600 家发卡机构参与；服务已覆盖全球超过 14 亿张 Visa 信用卡与借记卡（live for more than 1.4 billion Visa credit and debit cards）。
- Tap to P2P：该用例使用 tokenization，并结合 Tap to Consumer Device 与 Software Development Kit（SDK）实现设备间的接触式数据传输，同时利用 Visa Direct 的实时资金流动能力进行转账。
- Tap to Confirm：处于试点阶段；在高风险交易类型中，发卡机构可要求消费者“tap to confirm”，用于验证消费者持有实体卡。

#### Token 安全能力（Token Technology）

- Visa Token Service（VTS）：以 token 替代 16 位 Visa account number，并结合 surrogate account number、cryptographic information 等数据用于保护底层账户信息；截至 2025-09-30，“Visa has provisioned more than 16 billion tokens.”
- Visa Cloud Token Framework：云端安全技术项目，将 token 用例扩展至 mobile wallets、ecommerce platforms 与 Internet of Things devices，并增加 fraud mitigation 功能。
- Visa Payment Passkey：将 token 与消费者设备的 passkey 信息关联，用于增加支付体验的安全层。

#### A2A/开放银行与消费者支付触达（Expanding Our Reach in Consumer Payments）

- 【前瞻（原文）】“We aim to capture value and drive yield from CP currently routed through A2A networks via two primary strategies.”
- Visa Pay（2025）：通过 digital credentials 将参与的 digital wallets 连接至 Visa 网络；在部分地区，digital wallet providers、A2A schemes 与 banks 可通过 API 直接接入，以 white-label 方式在其应用内获取 Visa 的全球受理网络；并在 full stack SDK 中试点相同功能；在部分市场提供独立的 Visa Pay 应用以支持银行向其客户提供设置 Visa account/credential 并在 Visa 受理点完成支付的能力。
- Tink：在欧洲与拉美等地区作为开放银行解决方案，支持 open banking 与 A2A 交易的数据交换；自 2022 年收购后，open banking payments network 扩展至“thousands of bank connections”（截至 2025-09-30）。

#### 资金划转平台（Visa Direct）与 Visa+

- Visa Direct 平台：支持国内与跨境资金流动，客户可在网络中 collect、hold、convert、send funds；覆盖 P2P payments、A2A transfers、business/government payouts、seller settlements、refunds 等用例，覆盖超过 195 个国家和地区。
- 网络覆盖与端点：Visa Direct 使用超过 90 个 domestic payment schemes 与超过 60 个 card and wallet networks；“potential to reach approximately 12 billion endpoints”，由约 40 亿张 cards、bank accounts、digital wallets 构成。
- FY2025 运营规模：Visa Direct 处理交易超过 125 亿笔，合作伙伴超过 650 家。
- 【前瞻（原文）】“Through Visa+, we aim to provide simplified reach and delivery of funds through alias-linked accounts and wallets, giving flexibility and additional choices to consumers when receiving payments.”
- Visa+ 机制描述：Visa+ 不要求用户持有 Visa card；基于 alias credential，并与参与的 payment apps 绑定。

#### Value-Added Services（VAS）与商业化抓手

- 规模化空间口径：VAS “represents approximately a $520 billion annual revenue opportunity”；四个 portfolio 分别为 Issuing Solutions（约 $125B）、Acceptance Solutions（约 $95B）、Risk and Security Solutions（约 $150B）、Advisory and Other Services（约 $150B）。
- 【前瞻（原文）】“Our VAS strategy … has three areas of focus: (1) enhance Visa payments … (2) enable all payments … and (3) go beyond payments …”
- 截至 2025-09-30：已“offer more than 200 products and services”，并强调其中许多产品被设计为可协同工作。

#### 监管与合规约束（与产品扩张的耦合）

- 【前瞻（原文）】“new products and capabilities, including tokenization, push payments and cross-border money movement solutions could bring increased licensing or authorization requirements in the countries where the product or capability is offered.”
- 【前瞻（原文）】“As we continue to expand our capabilities and offerings in furtherance of our multi-year growth strategy, we will need to obtain new types …”
- 【分析】上述风险披露将“能力外延扩张”与“监管影响范围扩大/许可资质要求上升”直接绑定，意味着在 token、安全、A2A 与资金流动等方向的产品推进，商业化节奏与合规投入（牌照、授权、监督要求、治理与风控流程等）可能同步成为关键约束变量。

#### 关键术语说明

- Token（支付 token）
  - 原文引用：“VTS helps protect digital transactions by replacing 16-digit Visa account numbers with a token…”
  - 中文释义：以替代性凭证替换卡号用于支付与认证，降低卡号暴露与欺诈风险。
- A2A（Account-to-Account）
  - 原文引用：“A2A networks”
  - 中文释义：账户到账户的转账网络/支付路径，区别于基于卡网络的交易路径。
- VTS（Visa Token Service）
  - 原文引用：“Visa Token Service (VTS)… As of September 30, 2025, Visa has provisioned more than 16 billion tokens.”
  - 中文释义：Visa 的 token 服务体系，用于把卡号映射为 token 并在多场景中使用。
- Alias credential（别名凭证）
  - 原文引用：“alias credential that is linked to their participating payment apps”
  - 中文释义：以“别名”作为收款/到账标识，并与支付应用中的账户或钱包绑定，降低对卡号/卡网络端点的依赖。

### 证据与出处

- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Our Core Business | Tap to Pay / Tap to Phone / Tap to Add Card / Tap to P2P / Tap to Confirm
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Token Technology | Visa Token Service (VTS) / Visa Cloud Token Framework / Visa Payment Passkey
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Expanding Our Reach in Consumer Payments | Visa Pay / Tink / open banking payments network
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Visa Direct | platform description / coverage & endpoints / FY2025 volumes / Visa+
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Value-Added Services | $520B annual revenue opportunity / portfolios / “offer more than 200 products and services”
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Risk Factors | regulatory influence scope / “could bring increased licensing or authorization requirements” / multi-year growth strategy

---

## 收入结构与商业模式

### 结论要点

- 收入以支付网络服务为核心，按服务形态拆分为服务收入、数据处理收入、国际交易收入与其他收入；同时存在以“客户激励”形式对净收入的抵减项。
- 交易对价以可变为主，主要随交易的金额与类型、以及支付量等业务量指标变化；单项服务的交易价格按归属于该服务/费用的折扣净额列示。
- 支付网络服务的履约义务体现为“持续可用/随时可用”的网络与相关服务供给；各类收入通常在相关交易发生或服务提供的期间确认。
- 与客户/合作伙伴的激励安排以长期合同形式存在，既包括预付/固定激励（资本化并在合同期内摊销抵减净收入），也包括基于业绩目标的激励（按预计业绩计提负债并随实际表现调整）。

### 详细情况

#### 收入结构（按产品/地区/客户类型/渠道等公司披露维度）

- 收入类型拆分
  - 服务收入：支持客户使用 Visa 支付服务的相关服务收入。
  - 数据处理收入：围绕授权、清算与结算等处理环节，以及与发卡、受理、风险与身份等相关的增值服务、网络接入与维护支持等。
  - 国际交易收入：与跨境交易处理与货币兑换相关的收入。
  - 其他收入：主要来自咨询、营销与部分卡权益等增值服务，品牌/技术授权费，以及账户持有人服务、认证与许可等费用。
- 抵减项与净额呈现
  - 客户激励：向金融机构客户、商户及其他业务伙伴提供的现金与其他激励，目标指向支付量增长、受理范围扩大、使用推动与创新等；一般作为“客户激励”抵减净收入（若为换取客户提供的可区分商品/服务的现金支付，则归类为经营费用）。
- 客户类型与收费对象
  - 支付网络服务直接交付给发卡行与收单机构；这些参与方再将服务延伸到商户与消费者等网络参与者。净收入主要来自发卡行与收单机构。

#### 定价与计费方式（按产品/套餐/用量/席位/广告等）

- 对价特征
  - 对价以可变为主，主要随交易的金额与类型、以及 Visa 产品上的交易与支付量等业务量变化；单项服务的交易价格按归属于该服务/费用的折扣净额列示。
- 服务收入的计量节奏
  - 服务收入在季度层面主要以“当季定价 × 上季支付量”的方式评估（以客户上报的名义支付量为基础）。
- 其他类型收入的计量锚点
  - 数据处理收入与交易处理/信息处理相关服务强绑定；国际交易收入与跨境交易处理与货币兑换活动强绑定；其他收入与增值服务、授权与账户相关服务等绑定。

#### 合同与履约条款（期限、续费、折扣、返利、最低承诺、退款/违约等）

- 支付网络服务履约条款
  - 履约义务体现为为 Visa 品牌支付项目提供持续的网络接入与相关服务供给（“stand-ready”式持续服务）。
- 客户激励合同安排
  - 与金融机构客户、商户及其他业务伙伴存在长期合同，用于约定各类现金与非现金激励项目。
  - 预付与固定激励：在支付时通常资本化为客户激励资产，并在合同期内按直线方式摊销为对净收入的抵减。
  - 业绩目标激励：在满足/实现过程中按管理层对客户未来业绩的估计计入对净收入的抵减，并将未支付部分确认为客户激励负债；相关估计会随实际表现、合同修订与新合同签署等因素调整。

#### 收入确认关键点（与“会计政策”联动：履约义务、可变对价等）

- 确认原则与时点
  - 支付网络服务：在服务履行过程中确认（以预期可取得对价计量，净额列示销售税等类似税费）。
  - 数据处理/国际交易/其他收入：通常在相关交易发生或服务提供的同一期间确认。
- 主代理判断
  - 涉及第三方的安排，会评估是否在服务转移前取得对相关服务的控制权：作为主要责任方按总额确认；作为代理方按净额确认。
- 剩余履约义务披露豁免
  - 对支付网络服务及其他受客户未来表现约束、且对价可变的履约义务，采用可选豁免不披露相关剩余履约义务。

#### 客户生命周期与扩张路径（获客→转化→留存→扩张/流失，对应KPI）

- 客户与网络参与方的角色链条
  - 发卡行与收单机构是支付网络服务的直接交付对象，商户与消费者等作为网络参与方共同形成交易闭环。
- KPI 与收入联动的可观察锚点
  - 支付量：与服务收入的计量节奏直接相关（当季定价对上季支付量的应用）。
  - 交易发生与处理：与数据处理收入的确认期间一致（随交易发生/服务提供确认）。
  - 跨境交易：国际交易收入以跨境交易处理与货币兑换活动为核心，并在跨境交易发生/服务提供期间确认。
- 【分析】扩张路径更可能体现为
  - 在既有客户/网络参与方基础上，通过支付量提升、交易活跃度提升与跨境占比提升，带动支付网络相关收入增长；并通过增值服务叠加，提高每单位业务量的综合变现。

#### 关键术语说明

- Client incentives
  - 原文引用：Incentives are classified as reductions to net revenue within client incentives...
  - 中文释义：面向金融机构客户、商户及其他伙伴的激励安排，通常作为净收入的抵减项；少数在满足“以现金换取客户提供可区分商品/服务”的条件下转入费用。
- Service revenue
  - 原文引用：Current quarter service revenue is primarily assessed using a calculation of current quarter’s pricing applied to the prior quarter’s payments volume.
  - 中文释义：与客户使用支付服务相关的服务性收入，季度计量通常用“当季费率 × 上季支付量”作为主要评估方式。
- Principal / agent
  - 原文引用：...recognizes revenue on a gross basis, or the agent, and recognizes revenue on a net basis.
  - 中文释义：第三方参与的安排中，若在服务转移前取得控制权通常按总额确认；若仅撮合安排则按净额确认。

### 证据与出处

- SEC EDGAR | Form 10-K | Filed 2024-11-13 | Accession 0001403161-24-000058 | Item 8. Financial Statements and Supplementary Data | “Our net revenue in fiscal 2024 consisted of the following”（收入类型定义：Service revenue / Data processing revenue / International transaction revenue / Other revenue；以及 Client incentives 的用途描述）
- SEC EDGAR | Form 10-K | Filed 2024-11-13 | Accession 0001403161-24-000058 | Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations | Net revenues（表下注释：服务收入与名义支付量的季度评估关系）
- SEC EDGAR | Form 10-K | Filed 2024-11-13 | Accession 0001403161-24-000058 | Item 8. Financial Statements and Supplementary Data | Note 1—Summary of Significant Accounting Policies | Revenue Recognition（履约义务、可变对价、折扣净额、确认时点、主代理判断、剩余履约义务披露豁免）
- SEC EDGAR | Form 10-K | Filed 2024-11-13 | Accession 0001403161-24-000058 | Item 8. Financial Statements and Supplementary Data | Note 1—Summary of Significant Accounting Policies | Client incentives（长期合同、资产/负债确认与摊销/计提规则、例外情形转入费用）

## 关键经营指标（KPI）与口径字典

### 结论要点

- 核心KPI清单（按公司披露的经营驱动选择）：Payments volume（含 nominal/constant-dollar）、Processed transactions、（Nominal）Cross-border volume（ex-Europe）、Payment credentials、Merchant locations、Tap to Pay（面对面交易渗透）
- 指标定义与计算口径：Payments volume 与 Processed transactions 在 MD&A 中给出定义与口径（含汇率处理、是否包含现金交易、品牌范围等）；Cross-border volume 在已检索范围内未见明确“定义/计算公式”表述，仅作为解释变量被使用
- KPI与财务表/现金流的勾稽关系（领先指标/解释变量）：Payments volume ↔ Service revenue；Processed transactions ↔ Data processing revenue；（Nominal）Cross-border volume ↔ International transaction revenue；Payments volume ↔ Client incentives（净额收入的抵减项）

### 详细情况

- KPI字典（定义/口径 + 中文释义 + 跟踪意义）
  - Payments volume（含 Nominal payments volume）
    - 原文引用
      - “Payments volume is the primary driver for our service revenue, and the number of processed transactions is the primary driver for our data processing revenue.”
      - “Payments volume represents the aggregate dollar amount of purchases made with cards and other form factors carrying the Visa, Visa Electron, V PAY and Interlink brands and excludes Europe co-badged volume.”
      - “Nominal payments volume is denominated in U.S. dollars and is calculated each quarter by applying an established U.S. dollar/foreign currency exchange rate for each local currency in which our volumes are reported.”
    - 中文释义（口径）
      - 支付金额：以 Visa 体系内相关品牌（Visa/Visa Electron/V PAY/Interlink）的“购买交易”汇总金额计量；剔除 Europe co-badged volume
      - 名义口径（Nominal）：季度计算时以既定汇率将各币种交易量折算为美元
    - 【分析】跟踪意义
      - 作为 Service revenue 的核心解释变量；对净额收入与客户激励（Client incentives）的变动具有解释力
  - Processed transactions（Visa processed transactions）
    - 原文引用
      - “Processed transactions include payments and cash transactions, and represent transactions using cards and other form factors carrying the Visa, Visa Electron, V PAY, Interlink and PLUS brands processed on Visa’s networks.”
    - 中文释义（口径）
      - 处理笔数：包含“支付 + 现金”交易；统计在 Visa 网络上处理、且承载 Visa/Visa Electron/V PAY/Interlink/PLUS 品牌的交易
    - 【分析】跟踪意义
      - 作为 Data processing revenue 的核心解释变量；与网络处理能力、交易结构（支付/现金）相关
  - Total nominal volume / Cash volume（用于辅助理解 Payments volume 的组成）
    - 原文引用
      - “Cash volume generally consists of cash access transactions, balance access transactions, balance transfers and convenience checks.”
      - “Total nominal volume is the sum of total nominal payments volume and cash volume.”
    - 中文释义（口径）
      - 现金量（Cash volume）：主要由现金提取、余额查询、余额转移、便利支票等构成
      - 总量（Total nominal volume）：名义支付金额（payments）与现金量（cash）的加总
    - 【分析】跟踪意义
      - 便于拆解总量中“购买支付”与“现金相关交易”的结构变化，从而理解 payments volume 的变化质量
  - （Nominal）Cross-border volume（ex-Europe）
    - 原文引用
      - “International transaction revenue increased in fiscal 2025 over the prior year primarily due to growth in nominal cross-border volume of 13%, excluding transactions within Europe, …”
    - 中文释义（口径）
      - 已披露用于解释国际交易收入变动的“名义跨境交易量（剔除欧洲区内交易）”
    - 【占位符】
      - 缺口：Cross-border volume 的正式定义（统计对象、是否含现金、是否按交易发生地/发行地/收单地划分、是否按金额口径）、“excluding transactions within Europe”的边界口径
      - 需要：公司对 cross-border volume 的定义/计算说明（原文一句即可）及口径边界（尤其 Europe 内部交易的剔除规则）
      - 已检索范围：SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089（全文关键字检索：cross-border volume / cross-border transactions / excluding transactions within Europe；以及 Form 10-Q | Filed 2025-04-30 | Accession 0001403161-25-000037 同关键字检索）
      - 下一步：在其他年度 10-K/10-Q 的 MD&A 或“Key statistics/Volume”表格脚注中继续检索是否存在定义条款；若仍无，保留该指标为“解释变量”但不写计算口径
      - 【占位符：缺口】暂未在（已检索范围）中检索到公司披露/监管披露对该点的明确表述；以最终财报/监管披露为准。
  - Payment credentials
    - 原文引用
      - “... we had nearly 5 billion payment credentials, which are issued Visa card accounts, ...”
    - 中文释义（口径）
      - 支付凭证：已发行的 Visa 卡账户（issued Visa card accounts）；披露为规模型指标（nearly 5 billion）
    - 【分析】跟踪意义
      - 反映发卡侧覆盖与账户规模；可用于辅助理解交易笔数/支付金额的基数变化
  - Merchant locations
    - 原文引用
      - “... available to be used at more than 175 million merchant locations worldwide.”
    - 中文释义（口径）
      - 商户受理点：全球 merchant locations 的规模型指标（more than 175 million）
    - 【分析】跟踪意义
      - 反映受理网络覆盖；可用于辅助解释交易渗透率与增长空间
  - Tap to Pay（面对面交易渗透）
    - 原文引用
      - “Tap to Pay has become the default way Visa cardholders pay, comprising 79% and 66% of all face-to-face transactions, globally and in the United States in fiscal 2025, respectively.”
    - 中文释义（口径）
      - 非接触支付在面对面交易中的占比：全球与美国分别披露为 79%、66%（FY2025）
    - 【分析】跟踪意义
      - 反映线下支付行为迁移与技术渗透，可用于解释面对面交易结构变化与相关产品推进效果

- KPI与净收入科目勾稽（口径桥）
  - Service revenue ↔ Payments volume
    - 原文引用：“Service revenue in a given quarter is primarily assessed based on nominal payments volume in the prior quarter.”
  - Data processing revenue ↔ Processed transactions
  - International transaction revenue ↔（Nominal）cross-border volume（ex-Europe）
  - Client incentives ↔ Payments volume（量增往往带来激励规模变化，影响净额收入）

### 关键术语说明

- Payments volume / Nominal payments volume
  - 原文引用：“Nominal payments volume is denominated in U.S. dollars and is calculated each quarter by applying an established U.S. dollar/foreign currency exchange rate...”
  - 中文释义：名义支付金额为“美元计价的折算口径”，用于可比展示交易量
- Processed transactions
  - 原文引用：“Processed transactions include payments and cash transactions, ... processed on Visa’s networks.”
  - 中文释义：口径强调“是否由 Visa 网络处理”与“是否包含现金类交易”
- Payment credentials
  - 原文引用：“payment credentials, which are issued Visa card accounts”
  - 中文释义：支付凭证指已发行的 Visa 卡账户（账户数口径）
- Tap to Pay
  - 原文引用：“Tap to Pay has become the default way ... comprising 79% and 66% of all face-to-face transactions...”
  - 中文释义：非接触支付在面对面交易中的占比，用于衡量线下支付形态渗透

### 证据与出处

- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations — Payments volume and processed transactions（含：payments volume 定义、nominal 口径、processed transactions 定义；以及“service revenue / data processing revenue”的驱动关系与滞后期说明）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations — Net Revenue（含：international transaction revenue 与 nominal cross-border volume（ex-Europe）的关系、client incentives 与 payments volume 的关系表述）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | ITEM 1. Business（含：total payments and cash volume、payment credentials、merchant locations、Tap to Pay 渗透率等经营规模与采用率披露）

---

## 财务表现与盈利能力

### 结论要点

- FY2020–FY2025净收入从21,846百万美元增至40,000百万美元，FY2021–FY2025均实现同比增长（FY2025 +11.3%）。
- FY2020–FY2024运营利润率维持在约64%–66%，FY2025为60.0%；归母净利润率FY2025为50.1%（FY2024为55.0%）。
- 经营现金流与净利润整体匹配度较高（FY2021–FY2025约1.01x–1.26x），FY2025经营现金流23,059百万美元。

### FY2020–FY2024（完整财年）+ 最新已披露报告期的主要财务指标

#### **净收入（Net revenues）/增速**：

- 单位：百万美元；FY口径截至9月30日
- FY2020：21,846
- FY2021：24,105（+10.3%）
- FY2022：29,310（+21.6%）
- FY2023：32,653（+11.4%）
- FY2024：35,926（+10.0%）
- FY2025：40,000（+11.3%）

#### **运营利润（Operating Income）/增速**：

- 单位：百万美元
- FY2020：14,081
- FY2021：15,804（+12.2%）
- FY2022：18,813（+19.0%）
- FY2023：21,000（+11.6%）
- FY2024：23,595（+12.4%）
- FY2025：23,994（+1.7%）

#### **归母净利润（Net income attributable to common shareholders）/增速**：

- 单位：百万美元
- FY2020：10,866
- FY2021：12,311（+13.3%）
- FY2022：14,957（+21.5%）
- FY2023：17,273（+15.5%）
- FY2024：19,743（+14.3%）
- FY2025：20,058（+1.6%）

#### **经营现金流/增速**：

- 单位：百万美元
- FY2020：10,440
- FY2021：15,227（+45.9%）
- FY2022：18,849（+23.8%）
- FY2023：20,755（+10.1%）
- FY2024：19,950（-3.9%）
- FY2025：23,059（+15.6%）

#### 现金流质量（净利润→经营现金流的桥）

- 关键非现金项目（FY2025，单位：百万美元）：
  - 折旧摊销（Depreciation and amortization）：+1,220
  - 股权激励（Share-based compensation）：+897
  - 递延所得税（Deferred income taxes）：+152
  - 其他非现金项目（Other noncash income/expense）：-94
- 营运资本变动（FY2025，单位：百万美元）：
  - 应收账款变动（Accounts receivable）：+542
  - 其他经营资产变动（Other operating assets）：-160
  - 应付账款变动（Accounts payable）：+67
  - 应计负债及其他经营负债变动（Accrued liabilities and other operating liabilities）：-373
  - 客户激励变动（Client incentives）：+15,314

#### 经营现金流与净利润的匹配度

- FY2020：0.96x
- FY2021：1.24x
- FY2022：1.26x
- FY2023：1.20x
- FY2024：1.01x
- FY2025：1.15x

#### **毛利率**：

【占位符】
- 缺口：合并损益表未披露“毛利（Gross profit）/成本收入（Cost of revenues）/毛利率”口径，无法按常规定义直接计算毛利率。
- 需要：披露的毛利/成本收入行项目，或公司明确定义的毛利率/贡献利润率口径（如有）。
- 已检索范围：SEC EDGAR本地文件的FY2025、FY2024、FY2022 Form 10-K | Item 8 | Consolidated Statements of Operations。
- 下一步：在同一批披露文件中进一步检索MD&A或Non-GAAP指标处对替代利润率口径的定义，并在全篇保持一致口径。

#### **经营利润率**：

- FY2020：64.5%
- FY2021：65.6%
- FY2022：64.2%
- FY2023：64.3%
- FY2024：65.7%
- FY2025：60.0%

#### **归母净利润率**：

- FY2020：49.7%
- FY2021：51.1%
- FY2022：51.0%
- FY2023：52.9%
- FY2024：55.0%
- FY2025：50.1%

#### 费用率结构

##### **研发费用（R&D / Product development）/比率**：

【占位符】
- 缺口：未在合并损益表中检索到可直接对应“R&D / Product development”的单列费用项目。
- 需要：公司在损益表或附注中对研发/产品开发费用的单列披露，或与该口径的明确对应关系。
- 已检索范围：SEC EDGAR本地文件的FY2025、FY2024、FY2022 Form 10-K | Item 8 | Consolidated Statements of Operations。
- 下一步：在同一批披露文件中检索Operating expenses明细/按职能费用披露，确认是否存在可映射的口径并补齐。

##### **销售与市场费用（Sales and marketing）/比率**：

【占位符】
- 缺口：未在合并损益表中检索到可直接对应“Sales and marketing”的单列费用项目。
- 需要：公司在损益表或附注中对销售与市场费用的单列披露，或与该口径的明确对应关系。
- 已检索范围：SEC EDGAR本地文件的FY2025、FY2024、FY2022 Form 10-K | Item 8 | Consolidated Statements of Operations。
- 下一步：在同一批披露文件中检索费用分类口径说明（按职能/按性质），以确认可比口径并补齐。

##### **管理费用（General and administrative）/比率**：

- 单位：百万美元（比率为占净收入比例）
- FY2020：1,096（5.0%）
- FY2021：985（4.1%）
- FY2022：1,194（4.1%）
- FY2023：1,330（4.1%）
- FY2024：1,598（4.4%）
- FY2025：1,926（4.8%）

##### **运营费用合计（Total operating expenses）**：

- 单位：百万美元；按披露口径推算：运营费用合计 = 净收入 - 运营利润
- FY2020：7,765（占净收入35.5%）
- FY2021：8,301（占净收入34.4%）
- FY2022：10,497（占净收入35.8%）
- FY2023：11,653（占净收入35.7%）
- FY2024：12,331（占净收入34.3%）
- FY2025：16,006（占净收入40.0%）

#### 流动性与资本结构（Liquidity & Capital Structure）

- 现金与等价物：FY2025期末17,164；FY2024期末11,975（单位：百万美元）
- 有息负债与到期结构：FY2025长债合计25,171（其中一年内到期5,569；一年以上19,602）；FY2024长债非流动20,836（单位：百万美元）
- 股东回报与融资能力评估要点：
  - FY2025用于回购普通股18,316、支付股利4,634（单位：百万美元）
  - 【分析】以FY2025经营现金流规模与期末现金储备看，公司具备较强的股东回报与债务滚续资金来源；但FY2025利润率回落使对费用与资本配置效率的敏感性上升。

### 证据与出处

- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 8. Financial Statements and Supplementary Data | Consolidated Statements of Operations; Consolidated Statements of Cash Flows; Consolidated Balance Sheets
- SEC EDGAR | Form 10-K | Filed 2024-11-13 | Accession 0001403161-24-000058 | Item 8. Financial Statements and Supplementary Data | Consolidated Statements of Operations; Consolidated Statements of Cash Flows; Consolidated Balance Sheets
- SEC EDGAR | Form 10-K | Filed 2022-11-16 | Accession 0001403161-22-000081 | Item 8. Financial Statements and Supplementary Data | Consolidated Statements of Operations; Consolidated Statements of Cash Flows; Consolidated Balance Sheets

---

## 员工结构与组织能力

### 结论要点

- 员工规模在FY2025同比增长，自愿离职率维持在较低水平；人员分布覆盖多国家和地区且海外占比较高，对跨区域协同与管理能力提出更高要求。【分析】
- 组织能力建设侧重“人才发展+领导力培养+内部协作与知识工具”，并将GenAI能力嵌入员工工具与工作流，目标指向内容生产、效率与业务自动化提升。【分析】
- 人才竞争、关键管理层留任，以及移民/旅行/工作许可政策变化对跨辖区用工与调动的约束，是人才侧需持续跟踪的主要风险项。【分析】

### 详细情况

- 员工规模与分布
  - FY2025员工总数约34,100人，FY2024约31,600人，同比增加约8%。
  - 截至2025-09-30，自愿离职率（滚动12个月口径）约6%。
  - 员工分布在86个国家和地区，超过60%位于美国以外。【分析】在组织管理上更依赖跨时区协作机制、统一的领导力与文化框架、以及跨辖区用工合规能力的“系统化”建设。

- 人才发展与组织能力建设抓手
  - 学习发展与领导力培养：提供职业路径与学习支持，并通过教育资助项目与学习路径（Visa University learning pathways）等方式鼓励技能拓展；设置领导力发展项目（例如“New to Visa People Leadership”）。
  - GenAI能力嵌入：推动员工使用GenAI能力以提升内容创作、生产力与业务自动化；建设内部GenAI Hub，作为员工访问AI模型、应用与开发者工具的入口。
  - 文化与内部沟通：员工敬业度调研中，85%的员工愿意推荐Visa为“great place to work”；推动将VLPs融入员工体验的数字化活动；上线面向各层级管理者的沟通工具与People Leader Hub；内部社交网络Viva Engage月度访问覆盖95%员工，其中89%每月阅读六条或以上内容；企业内网现代化以支持GenAI工具集成与个性化内容分发。

- 人才与用工相关风险提示
  - 【前瞻（原文）】“We may be unable to attract, hire and retain a highly qualified workforce, including key management.”
  - 【前瞻（原文）】“Ongoing changes in laws and policies regarding immigration, travel and work authorizations … could continue to impair our ability to attract, hire and retain qualified employees.”
  - 【前瞻（原文）】“… could impact our workforce development goals, impact our ability to achieve our business objectives, and adversely affect our business and our future success.”
  - 【分析】上述风险与“员工规模扩张+海外分布占比高”的组织形态相叠加时，关键观察点包括：关键岗位供给与替代性、跨辖区调动的合规与效率、以及管理层继任安排对组织韧性的支撑强度。

#### 关键术语说明

- GenAI
  - 原文引用：“GenAI capabilities… enhance content creation, productivity and business automation.”
  - 中文释义：生成式人工智能能力，用于辅助内容生成、提升效率与推动流程自动化。
- attrition（voluntary workforce turnover）
  - 原文引用：“voluntary workforce turnover (rolling 12-month attrition)”
  - 中文释义：员工离职率（此处为自愿离职，且为滚动12个月口径）。

### 证据与出处

- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Part I, Item 1. Business | Talent and People
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Part I, Item 1A. Risk Factors | We may be unable to attract, hire and retain a highly qualified workforce, including key management.

---

## 子公司、分公司与关联公司及集团架构

### 结论要点

- 本报告口径中，“Visa/我们/公司”指 Visa Inc. 及其子公司；集团层面以合并口径编制财务报表并抵销内部往来。
- 合并范围以“控制性财务利益”为核心，并覆盖公司作为主要受益人的 VIE；披露期内公司在 VIE 的投资对合并财务报表不构成重大影响。
- 与美国历史诉讼相关的回溯性责任安排涉及多项协议与多类主体（含 Visa U.S.A. Inc. 及 Visa International Service Association 等）；在本地材料范围内无法形成“截至 FY2025 的完整子公司/分支机构清单”，需保留缺口占位符。

### 详细情况

- 披露口径与集团边界
  - 文本口径：除非上下文另有说明，“Visa/我们/公司”指 Visa Inc. 及其子公司。
  - 会计口径：合并财务报表包含 Visa 及其合并实体；集团合并范围覆盖公司具有控制性财务利益的实体，以及公司作为主要受益人的 VIE；内部余额与内部交易在合并中抵销。

- “集团架构”的可核查表达（以法律实体与会计边界为主）
  - 顶层：Visa Inc. 作为集团报告主体。
  - 合并层：以“控制性财务利益 + VIE 主要受益人”界定纳入合并的实体集合（本地材料未提供合并范围内法律实体的完整列示）。
  - 投资/关联层：公司对不控制但能施加重大影响的被投资实体适用权益法；对既不控制亦无重大影响的部分股权投资适用公允价值计量替代法（会计政策层面的“关联/被投”边界描述，不等同于法律意义上的关联方名录）。

- 重要法律实体与安排（基于披露出现频次与对集团风险/义务的重要性，非穷举）
  - Visa U.S.A. Inc.（Visa U.S.A.）
    - 在美国回溯性责任安排中出现，涉及成员的赔付/补偿义务执行机制（含基于其公司章程、细则与会员协议的执行）。
  - Visa International Service Association（Visa International）
    - 与 Visa U.S.A. 一同作为协议主体参与“interchange judgment sharing agreement”；并与 Visa U.S.A. 一同出现在“loss sharing agreement”的协议安排中。

- 【占位符】
  - 缺口：截至 FY2025（或最近报告期）的“子公司/分公司（分支机构）/关联公司”完整清单，以及可复核的集团法律实体结构图（含各实体注册地/持股关系/是否合并等）。
  - 需要：Form 10-K 中 Exhibit 21（Subsidiaries of the Registrant）或等效的法律实体清单披露；如有，补充分支机构（branch/office）清单与股权法/非控制投资的主要被投主体列表（以公司披露为准）。
  - 已检索范围：`filings/V/10-K_2025-11-06_report_2025-09-30_0001403161-25-000089/v-20250930.htm`（含 Item 8 的合并政策与相关注释段落）；以及材料清单所列的其他本地 10-K/10-Q 主文档（未见可直接抽取的 FY2025 子公司清单披露）。
  - 下一步：在本地材料范围内补齐 Exhibit 21（若已下载但未在清单中列示，需定位对应文件）；否则待补充材料后回填本章“子公司/分支机构/关联公司”清单与结构。

### 证据与出处

- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Front Matter | Defined terms（“Unless the context indicates otherwise… Visa Inc. and its subsidiaries.”）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 8 | Note 1—Summary of Significant Accounting Policies | Consolidation and basis of presentation（控制性财务利益、VIE 主要受益人、内部往来抵销、VIE 投资重大性表述）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 8 | Notes to consolidated financial statements | Indemnification obligations / Interchange judgment sharing agreement / Loss sharing agreement（涉及 Visa U.S.A. Inc. 与 Visa International Service Association）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 8 | Note 1—Summary of Significant Accounting Policies | Non-marketable equity securities / Equity method of accounting / Fair value measurement alternative（权益法与非控制股权投资会计边界）

---

## 所属行业分类与相关产业政策

### 结论要点

- 【分析】结合披露的业务形态（以专有先进交易处理网络 VisaNet 为核心、提供支付网络与相关解决方案/服务），公司可归入“支付网络/支付技术基础设施”赛道。
- 公司披露其业务处于多司法辖区监管框架之下；与支付行业直接相关的规则（如欧洲 IFR、PSD2）以及数据与隐私/AI/网络安全、反洗钱与制裁等横向合规要求，共同构成对业务运营的重要外部约束。
- 【前瞻】披露中提示：部分监管框架及监管变化可能带来支付处理方式、客户接口要求、认证流程与数据处理要求的调整，并可能影响竞争格局与运营复杂度。

### 详细情况

- 行业定位（按业务形态归类）
  - 公司以专有先进交易处理网络 VisaNet 为核心，定位为“payments technology company”，并描述其用于通过多种形态与技术连接多端点、支持资金流转与支付交易处理。
  - 【分析】从“网络连接与交易处理能力”出发，公司更接近支付产业链中提供网络与处理能力的平台型基础设施（而非以利差/信贷为核心的传统金融机构形态）；因此监管议题更多体现为支付规则、数据与金融犯罪合规等横向监管集合。

- 相关产业政策/监管框架（按披露的重要主题归纳）
  - 政府监管总体框架
    - 公司披露其作为全球支付技术公司，业务在各司法辖区受到复杂且持续演进的监管约束，并在年度报告中单列“GOVERNMENT REGULATION”讨论主要监管主题。
  - 支付行业规则：欧洲 IFR、PSD2（示例）
    - 【前瞻】披露提到：作为欧洲 IFR 相关监管环境的一部分，可能面临来自其他网络、处理方或第三方的竞争压力，且存在由其他主体直接处理 Visa 交易的情形。
    - PSD2：披露提到 PSD2 对金融机构客户提出客户账户访问权相关要求；同时 PSD2 的强客户认证要求在披露中被描述为【前瞻】可能带来运营复杂度并影响消费者支付体验。
  - 数据、隐私、AI 与网络安全
    - 公司披露其运营受日益复杂且碎片化的数据相关监管影响，主题涵盖隐私、数据使用、AI 与网络安全，并会影响其数据处理方式及产品/服务运营。
    - 【前瞻】披露提到：全球立法与监管机构正在提出新的法律或监管要求，这些变化可能要求更严格的数据收集与处理实践、扩展网络安全要求、限制跨境数据流动、影响先进 AI 系统的采用，并对处理个人数据的企业增加义务。
    - GDPR：披露提到欧洲数据保护机构持续执行 GDPR，并存在创纪录罚款案例。
  - 反洗钱、反恐融资与制裁/反贿赂等合规
    - 公司披露其受反贿赂、反洗钱、反恐融资与制裁等法律法规约束（包含美国 Bank Secrecy Act 与 OFAC 相关制裁项目），并据此对部分受全面制裁覆盖的国家/地区或被列入制裁名单的主体采取限制性政策。

#### 关键术语说明

- VisaNet
  - 原文引用：proprietary advanced transaction processing network, VisaNet
  - 中文释义：公司披露的专有交易处理网络名称，用于承载其支付交易处理与相关网络服务。
- IFR
  - 原文引用：Interchange Fee Regulation (IFR)
  - 中文释义：公司披露中用于指代欧洲一项与支付卡相关的监管框架缩写，本章仅用于标识该监管框架。
- PSD2
  - 原文引用：second Payment Services Directive (PSD2)
  - 中文释义：公司披露中用于指代欧盟第二版《支付服务指令》的缩写，本章仅用于标识该监管框架。
- GDPR
  - 原文引用：General Data Protection Regulation (GDPR)
  - 中文释义：公司披露中用于指代欧盟《通用数据保护条例》的缩写，本章仅用于标识该监管框架。
- OFAC
  - 原文引用：Office of Foreign Assets Control (OFAC)
  - 中文释义：公司披露中用于指代美国财政部负责经济与贸易制裁项目的机构缩写，本章仅用于标识相关制裁合规框架。

### 证据与出处

- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1. Business | Business overview（含 VisaNet、支付技术公司定位相关表述）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1. Business | GOVERNMENT REGULATION（含“global payments technology company”与主要监管主题提示）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1. Business | GOVERNMENT REGULATION（Europe: Interchange Fee Regulation (IFR)、second Payment Services Directive (PSD2)、strong customer authentication 相关段落）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1A. Risk Factors | Privacy, Data Use, AI and Cybersecurity（含“proposing new laws or regulations…could require…”段落、GDPR 执法与罚款描述）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1A. Risk Factors | Regulatory / Compliance risks（含 Bank Secrecy Act、OFAC sanctions、反贿赂/反洗钱/反恐融资等合规约束与限制性政策表述）

---

## 经营理念与战略

### 结论要点

- 经营理念以“最佳支付与收款方式”为导向，强调通过可信、可靠与高效的网络促进全球商业与资金流动。
- 战略框架围绕“收入增长驱动 + 底座能力加固”：以消费支付、商业与资金流动解决方案、增值服务为三条增长主线，同时强化品牌、产品创新、平台与安全等关键基础能力。
- 执行路径强调从卡基消费支付向非卡形态延伸，并通过跨境能力、代币化与“Tap to Everything”等产品与技术投入扩大交易范围与应用场景。
- 风险与约束方面，将并购/合资/战略投资作为战略工具之一，但相关整合与协同不确定性被纳入关键风险框架；同时把网络安全视为“信任”的关键组成并纳入企业风险管理。

### 详细情况

- 经营理念与定位
  - 以数字支付为核心业务定位，围绕“促进安全、可靠与高效的全球商业与资金流动”构建价值主张。
  - 明确目的表述：提升“每个人、每个地方”的支付与收款体验，目标是成为“最佳支付与收款方式”。

- 战略框架与增长主线
  - 【分析】战略表述呈现“增长抓手分层+底座能力护航”的结构：一方面以三条业务主线推动收入增长，另一方面通过对品牌、产品创新、平台与安全等基础能力投入来支撑执行与长期竞争力。
  - 增长主线（战略表述的三类业务方向）
    - 消费支付（CP）：强化卡基消费支付影响力，并扩展至非卡支付形态；重点投入“Tap to Everything”、代币技术、跨境能力等，以扩大交易与凭证使用场景。
    - 商业与资金流动解决方案（CMS，原“new flows”）：推动商业支付与资金流动渗透提升。
    - 增值服务（VAS）：通过创新服务加深与客户的合作关系。

- 关键能力与投入方向（与战略执行直接相关）
  - 跨境（Cross-Border）
    - 将跨境旅行与电商等场景作为重要抓手之一，强调以风险管理、反欺诈与代币化等能力形成差异化，并推进跨境货币与结算能力（含外汇解决方案）。
    - 战略动作聚焦于扩展跨境网络的覆盖与效用、提升重点走廊的使用与受理点、增强旅行与电商价值主张、提升跨境交易性能与授权率，并拓展多币种支付凭证等功能。
  - “Tap to Everything”与代币化
    - 围绕“Tap to Pay”向更多“Tap”用例延伸（如Tap to P2P等），并将代币化作为安全与体验的重要技术支撑；在部分用例中结合Visa Direct的实时资金流动能力实现转账/拨付等功能。
  - “Network of networks”与连接方式
    - 强调以单一连接点支持不同网络起止端的资金流动，覆盖P2P、B2C、B2B、G2C及C2B等支付形态，以应对支付生态复杂性并扩大可服务端点。

- 战略底座与治理关注点
  - 关键基础能力加固
    - 明确将品牌、产品创新、平台与安全、政府事务、销售与服务、人才与组织等视为业务模型的关键基础能力，用于支撑战略执行与目的实现。
  - 网络安全与信任
    - 将“信任”视为不可或缺资产，认为强网络安全项目是维系信任的关键要素；将网络安全风险纳入企业风险管理框架进行识别、评估与管理。
  - 外延工具与风险边界
    - 将并购、战略投资与合资作为整体业务战略的一部分；同时提示可能无法实现预期收益且伴随显著风险与不确定性。

### 证据与出处

- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1. Business | OVERVIEW（purpose表述、业务定位与资金流动/全球商业叙述）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1. Business | Our Strategy（“accelerate revenue growth through CP/CMS/VAS + fortify foundations”的战略框架及对CMS/VAS的定义性表述）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1. Business | Consumer Payments（“We aim to grow CP…”及对Tap to Everything、token technology、cross-border capabilities等投入方向）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1. Business | Tap to Everything（Tap to Pay与“Tap to Everything”扩展用例、Tap to P2P与Visa Direct结合的产品叙述）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1. Business | Cross-Border（跨境差异化能力与“strategic initiatives”的投入方向叙述）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1. Business | Fortify key foundations（关键基础能力构成：brand、product innovation、platforms and security、government affairs、sales and service、talent and people）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1. Business | OVERVIEW（network of networks strategy：单一连接点与多类支付形态覆盖）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1C. Cybersecurity | Visa’s Approach to Cybersecurity（信任、网络安全项目与企业风险管理框架的关系）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1A. Risk Factors | Structural and Organizational Risks（并购/合资/战略投资作为战略工具及其预期收益不达成风险）

---

## 会计政策与关键科目口径

### 结论要点

- 收入确认以“支付网络服务+增值服务”为核心，交易对价多为与交易量/支付量相关的可变对价；其中服务收入存在“当季定价×上季支付量”的计算滞后特征，影响季度可比性。
- 财务工具相关的会计波动主要来自外汇衍生品与套期会计：现金流套期的公允价值变动进入其他综合收益，满足条件时再重分类进损益；部分衍生品未指定套期会计时，其公允价值变动计入管理费用。
- 无形资产与商誉的关键在于减值测试：有限寿命无形资产按直线法摊销并在减值迹象下测试；无限寿命无形资产与商誉不摊销、按年度（或更频繁）进行减值评估。
- 租赁会计以使用权资产与租赁负债为核心，贴现率与“合理确定”续租/终止选择权判断会影响负债规模与费用节奏。
- 2025 财年采用 ASU 2023-07（分部披露增强），带来分部披露信息增加。

### 关键会计政策与可比性风险点

#### 收入确认政策

- 支付网络服务的对价多为可变对价，主要与交易金额/交易类型及 Visa 产品的支付量相关；收入以“服务履约”过程中确认，并以预计可收取对价计量（净额口径扣除销售税及类似税费）。
- 对涉及第三方的安排，会区分“作为主要责任方（按总额确认）”或“作为代理（按净额确认）”。
- 服务收入主要由支持客户使用支付服务的相关服务构成，包含与支付量相关的费用；核心履约义务为持续提供对 Visa 支付网络及相关服务的访问能力。服务收入的当季计量口径以“当季定价应用于上季支付量”为主。
- 数据处理收入（授权、清算、结算等及部分增值服务等）与国际交易收入（跨境处理与货币转换）一般在相关交易发生或服务履约的同一期间确认。
- 【分析】服务收入的“上季支付量”计量口径会引入确认滞后：当支付量结构或定价在季度间发生变化时，收入与当期经营活动的同步性下降，季度同比/环比解读需显式考虑该滞后。

#### 财务工具与公允价值测量

- 衍生工具以公允价值列示，并以“总额”方式在资产负债表列报；外汇远期用于对冲以外币计价的特定货币性资产与负债的汇率波动。未指定套期会计的衍生工具公允价值变动计入一般及管理费用。
- 现金流套期的衍生工具公允价值变动计入其他综合收益；当被套期的预测交易发生并进入损益时，相关累计其他综合收益按对应收入/费用科目重分类至损益。
- 公允价值套期与净投资套期：公允价值套期的套期工具损益及被套期项目公允价值变动计入利息费用；净投资套期相关损益计入其他综合收益。
- 债务工具在资产负债表按摊余成本计量；其披露的估计公允价值主要由第三方定价机构基于活跃市场中相似（但非完全相同）工具的报价等信息提供，若按公允价值计量通常落在公允价值层级 Level 2。
- 【分析】套期指定与有效性评估、以及“OCI→损益”的重分类节奏，会改变利润表与其他综合收益之间的波动分布；同时，第三方定价与 Level 2 估值输入会影响公允价值披露的可比性与敏感度。

#### 商誉与无形资产的摊销与减值

- 可辨认无形资产在并购日按公允价值入账并评估使用寿命；有限寿命无形资产以客户关系为主，按直线法摊销，使用寿命区间为 5–15 年，并在出现减值迹象时进行可收回性评估与减值测试。
- 无限寿命无形资产包括 Visa 商号、客户关系与再取得权利等，不摊销；按年度或在出现减值迹象时更频繁进行减值评估，可先进行定性评估决定是否需要定量测试；当公允价值低于账面价值时确认减值。
- 商誉为并购对价超过可辨认净资产公允价值的部分，不摊销；按报告单位层级进行年度（或更频繁）减值测试。披露口径下，2025 财年年度减值评估结论为未发生减值，且截至 2025-09-30 未出现新的减值迹象。
- 【分析】无形资产/商誉减值测试依赖估值假设与经营预期，若外部环境或关键假设变化，可能出现离散的减值费用，进而影响期间可比性。

#### 税务处理与所得税

- 所得税采用资产负债法：递延所得税资产/负债反映账面价值与计税基础差异及亏损/抵免结转的未来税务影响，并以已颁布税率计量；当递延所得税资产“更可能不实现”时计提估值备抵。
- 对税法解释存在不确定性时，会对所得税不确定性进行确认、计量与披露；不确定税务事项相关利息费用计入“interest expense and investment income (expense)”，相关罚款计入“other”。
- 【分析】估值备抵与不确定税务事项的确认/计量属于管理层判断较强领域，可能造成有效税率与期间所得税费用的波动。

#### 外币汇率与跨境交易

- 当功能货币非美元时，资产负债表项目按期末汇率折算，收入与费用按期间平均汇率折算；折算差额计入累计其他综合收益（损失）。
- 【分析】跨境业务与多币种资产负债带来“利润表经营波动”与“权益端折算差额（AOCI）”的双通道影响；两者口径不同，解读时需区分经营性影响与折算性影响。

#### 租赁会计

- 在合同开始时判断安排是否包含租赁；使用权资产与租赁负债在租赁开始日确认，并以剩余租赁付款额在租赁期内的现值计量（仅纳入开始日固定且可确定的付款）。贴现率以租赁开始日的增量借款利率为主。
- 使用权资产包含租赁开始日前支付的租赁款，并扣除已取得的租赁激励；租赁期在“合理确定将行使”续租/终止选择权时纳入相应期限。
- 租赁期不超过 12 个月的租赁不确认使用权资产与租赁负债；租赁与非租赁组成部分不合并，非租赁组成部分主要为维护与公用事业等。
- 使用权资产列示于“other assets”；租赁负债流动部分列示于“accrued liabilities”，长期部分列示于“other liabilities”。租赁成本主要计入一般及管理费用，并包含租赁协议下确认的金额（结合减值与转租收入调整）。
- 【分析】增量借款利率、租赁期判断（续租/终止选择权“合理确定”）与租赁/非租赁拆分，会共同影响确认时点、负债规模与费用节奏，跨期可比性需关注关键假设是否变动。

#### 股权激励与员工福利

- 每股收益采用两类法（two-class method），以反映不同类别普通股与参与证券的权利差异；参与证券包括优先股以及带有不可没收分红或分红等价权利的限制性股票单位（RSUs）。
- 养老金与其他退休后福利：美国养老金计划对新参与者关闭且已冻结；披露口径下，2025 年 6 月美国合格确定给付养老金计划修订为在 2025-09-30 终止生效（终止仍需监管审批），且终止不会降低参与者福利。
- 【前瞻（原文）】“Upon the settlement of pension obligation under the plan, which is currently expected in 2027, … a settlement gain or loss will be recognized …”
- 【前瞻】若后续按计划完成养老金义务结算并确认结算损益，可能对结算当期利润表形成一次性波动，需在利润质量与可持续性分析中剥离该类事项。

### 证据与出处

- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Note 1—Summary of Significant Accounting Policies（Revenue from Contracts with Customers; Derivative and hedging instruments; Foreign currency transactions and translations; Intangible assets, net and goodwill; Leases; Income taxes; Earnings per share; Recently adopted accounting pronouncement）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Note 3—Revenue
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Fair Value Disclosures（Other Fair Value Disclosures—Debt; Other financial instruments not measured at fair value）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Lessee Operating Leases
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Note 11—Pension and Other Postretirement Benefits

---

## 税收政策与政府优惠政策

### 结论要点

- 2025财年有效所得税率为17%（2024财年17%，2023财年18%）；有效税率与税费主要受境外税务影响、州税、审计结案与特定费用税务处理等调节项影响。
- 新加坡税收激励适用于亚太地区运营枢纽，有效期至2028-09-30，且需满足特定条件；2025/2024/2023财年分别减少新加坡税费$453 million/$419 million/$468 million，对稀释每股收益的税收激励毛受益分别为$0.23/$0.21/$0.22。
- 截至2025-09-30，外国净经营亏损结转约$1.1 billion，可无限期结转；2025与2024财年的估值备抵主要与近年收购子公司的外国净经营亏损相关。
- 不确定税务事项方面：截至2025-09-30/2024-09-30计提利息$160 million/$300 million，且未计提重大应计罚金；美国联邦、加州与印度等地仍存在在审/申诉事项。

### 详细情况

- 有效税率与调节项（截至各财年9月30日，单位：$ million，括号为税收收益；百分比为对有效税率的影响）
  - 所得税费用：2025财年$4,136（17%）；2024财年$4,173（17%）；2023财年$3,764（18%）
  - 美国联邦法定税率（21%）对应税额：2025财年$5,081（21%）；2024财年$5,022（21%）；2023财年$4,418（21%）
  - 州税（扣除联邦抵减）：2025财年$244（1%）；2024财年$258（1%）；2023财年$245（1%）
  - 境外税务影响（扣除联邦抵减）：2025财年（$775）（-3%）；2024财年（$828）（-4%）；2023财年（$758）（-3%）
  - 不确定税务事项再评估：2023财年（$142）（-1%）
  - 审计结案：2024财年（$223）（-1%）
  - 特定费用的税务处理：2025财年（$263）（-1%）
  - 其他净额：2025财年（$151）（-1%）；2024财年（$56）（约0%）；2023财年$1（约0%）
- 新加坡税收激励（政府优惠政策）
  - 适用对象：亚太地区运营枢纽
  - 有效期：至2028-09-30（附条件要求）
  - 影响口径：2025/2024/2023财年分别减少新加坡税费$453 million/$419 million/$468 million；对稀释每股收益的税收激励毛受益分别为$0.23/$0.21/$0.22
- 递延所得税、估值备抵与亏损结转
  - 估值备抵：2025财年$264 million；2024财年$212 million（主要与近年收购子公司的外国净经营亏损相关）
  - 截至2025-09-30：外国净经营亏损结转约$1.1 billion，可无限期结转
- 不确定税务事项（Uncertain tax positions）
  - 未确认税收利益（截至2025-09-30/2024-09-30/2023-09-30，不含利息与罚金）：$1.7 billion/$3.8 billion/$3.5 billion；其中若确认将降低未来期间有效税率的金额分别为$1.5 billion/$1.4 billion/$1.6 billion
  - 与不确定税务事项相关的净利息费用：2025财年（$140 million）；2024财年$29 million；2023财年$34 million
  - 截至2025-09-30/2024-09-30：计提利息$160 million/$300 million，且未计提重大应计罚金
- 税务审计、争议与申诉进展（节选）
  - 美国联邦：2025财年，美国国税局完成对2016–2018财年美国联邦所得税申报的现场工作；2008–2018财年仍存在与部分所得税扣除相关的未决事项；针对2008–2015财年相关事项已向美国联邦索赔法院提起诉讼以挑战国税局立场
  - 加州：2012–2015财年所得税检查已于2025财年结束，并就相关年度退款申索提起行政申诉；2016–2021财年所得税申报正在接受检查
  - 印度：税务机关已完成对2019–2023财年期间相关纳税年度的评税；已提出异议并向上诉机关提起上诉
- 【分析】税收激励、审计结案与特定费用税务处理等项目对有效税率与每股收益的影响可直接对照披露的调节项金额与每股毛受益；其可持续性取决于激励条件满足、审计/申诉推进与不确定税务事项的后续处理。
- 【分析】在审/申诉与未决扣除事项的最终解决时间与结果存在不确定性；对未确认税收利益在未来12个月的增减亦无法合理估计，建模时宜保留对税费与现金税的敏感性区间。

### 证据与出处

- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 8 | Note 19—Income Taxes | Effective income tax rate reconciliation & tax provision
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 8 | Note 19—Income Taxes | Singapore tax incentive (term, conditions, tax and EPS impact)
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 8 | Note 19—Income Taxes | Deferred taxes, valuation allowance, foreign NOL carryforwards
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 8 | Note 19—Income Taxes | Unrecognized tax benefits, interest/penalties, tax examinations and disputes

---

## 重大诉讼与法律程序

### 结论要点

- FY2025 10-K 的 Item 3 未单列展开重大法律程序，核心信息集中在财务报表附注 Note 20（Legal Matters）的分项披露与诉讼准备金口径。
- FY2025 期末累计诉讼准备金（accrued litigation）为 $3,033 million（FY2024：$1,727 million），其中 U.S. covered litigation 期末为 $2,698 million（FY2024：$1,537 million），主要与 interchange MDL 相关。
- 美国司法部（DOJ）于 2024-09-24 提起 Sherman Act 诉讼，2025-06-23 法院驳回撤诉动议；相关商户/持卡人集体诉讼同步推进并出现“部分准许、部分驳回”的程序性结果。
- 欧洲侧存在收单机构费用监管调查、德国 ATM 相关争议与瑞士 interchange 诉讼等事项，叠加美国反垄断诉讼，构成主要法律不确定性来源。

### 详细情况

- 披露口径与范围
  - Item 3（Legal Proceedings）以交叉引用方式指向 Item 8 财务报表附注 Note 20（Legal Matters）。
  - Note 20 覆盖诉讼与监管程序的主要类别、关键进展节点、以及诉讼准备金（covered / uncovered）计量与变动。

- 诉讼准备金（单位：百万美元，$ in millions）
  - 累计诉讼准备金期末余额：FY2025 为 $3,033；FY2024 为 $1,727。
  - U.S. covered litigation 期末余额：FY2025 为 $2,698；FY2024 为 $1,537；FY2025 期间“provision for interchange multidistrict litigation”为 $2,210，期间支付（payments for U.S. covered litigation）为 $1,049。
  - FY2025 期间记录 additional accruals of $2.2 billion，并向 U.S. litigation escrow account 存入 $875 million，用于 interchange MDL 相关索赔安排。

- 美国 interchange MDL（MDL 1720）及相关商户诉讼
  - 2005 年起商户在联邦法院起诉并整合至纽约东区（MDL 1720），争议焦点包括 interchange reimbursement fees、no-surcharge、honor-all-cards、交易费等规则/费率安排及反垄断主张。
  - 2012 Settlement Agreement：从 U.S. litigation escrow account 存入约 $4.0 billion，并另存入约 $500 million（与八个月 interchange reductions 相关）；并收到 takedown payments 约 $1.1 billion 回存托管账户。2016-06-30 第二巡回法院撤销商户集体认证并撤销和解批准并发回重审。
  - 2018-09-17 Amended Settlement Agreement（Damages Class）：要求被告追加支付合计 $900 million，其中 Visa 份额 $600 million（来自 litigation escrow account）；2019-12-13 地方法院最终批准，2023-03-15 第二巡回法院维持最终批准。因 opt-out 比例，$700 million 返还被告；Visa 份额 takedown payment 约 $467 million 回存托管账户。
  - Injunctive Relief Class：2024-03-25 与 Mastercard 达成和解协议；2024-06-25 初步批准动议被驳回。
  - Individual Merchant Actions：2013 年以来出现 50+ 案件（含借记卡相关市场、chip-and-PIN、交易费与规则等争议），部分请求禁令与损害赔偿。

- 美国反垄断调查/诉讼与衍生集体诉讼（借记网络）
  - DOJ 调查与诉讼：2012-03-13 起收到 CID（后续 2021、2023 多次 CID），关注 U.S. debit 与竞争议题；2024-09-24 DOJ 在纽约南区提起 Sherman Act 诉讼，指控在 general purpose debit network services 与 card-not-present debit network services 市场的垄断/尝试垄断及不合理限制竞争；2025-06-23 撤诉动议被驳回。
  - U.S. Debit Class Actions：自 2024-10-01 起多起集体诉讼并在纽约南区集中；2024-12-16（商户）与 2024-12-27（持卡人）分别提交合并修订起诉；2025-02-24 提交撤诉动议，2025-10-29 结果为“部分准许、部分驳回”；另有强制驳回特定主张的动议被驳回并进入第二巡回上诉程序。
  - Debit Surcharge Class Action：2024-12-04 在加州北区起诉，争议围绕未执行禁止 surcharging 规则；2025-05-28 撤诉动议获准，后续提交修订起诉并继续推进（截至 2025-07-23 已提交新的撤诉动议）。
  - U.S. Securities Class Action / Derivative：2024-11-20 起在加州北区提起证券集体诉讼（覆盖 2023-03-02 至 2024-09-23），指向与 DOJ 诉讼相关做法的披露问题；2025-09-12 已提交 dismiss/strike 动议。2025 年一季度起另有多起股东衍生诉讼并同意中止以等待证券案撤诉结果。

- 欧洲及其他地区事项
  - European Commission Acquirer Fees Investigation：2024-08-30 启动对收单机构费用的初步调查。
  - German ATM Litigation：自 2021-12 起德国银行起诉，主张 ATM 规则限制国内取现 access fees 属反竞争并多请求损害赔偿；管辖权抗辩出现分化结果并进入上诉，另有一项在德国联邦法院待决。
  - Europe Interchange Litigation（瑞士）：2025-06-20 瑞士商户在苏黎世商事法院起诉，主张瑞士 interchange fees 限制竞争并请求自 2022-06-01 起的损害赔偿。
  - Income Tax Litigation：2024-06-21 在美国联邦索赔法院起诉美国政府，争议 2008–2015 年与软件相关的所得税扣除被 IRS 否决。

- 【分析】FY2025 诉讼准备金的显著抬升与 interchange MDL 相关的新增计提/托管存入相呼应，说明部分历史性争议进入更可计量的损失确认阶段；与此同时，DOJ 诉讼与 U.S. Debit Class Actions 的程序性推进意味着竞争与费率/规则相关的法律不确定性仍可能对业务条款与合规成本形成外溢压力。

### 证据与出处

- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 3. Legal Proceedings
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 8. Financial Statements and Supplementary Data | Notes to Consolidated Financial Statements | Note 20—Legal Matters
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 8. Financial Statements and Supplementary Data | Notes to Consolidated Financial Statements | Note 5—U.S. and Europe Retrospective Responsibility Plans

---

## 竞争对手与同业对比分析

### 结论要点

- 竞争不局限于卡组织网络：除全球/跨区域卡组织外，还包括地方/区域网络、RTP 网络、数字钱包、支付处理商，以及电商/BNPL/加密货币（含 stablecoins）等替代支付与商业支付解决方案；监管演进可能通过“本地网络/本地处理”改变竞争与价值链分工。【分析】
- 在 calendar year 2024 的“网络对比表口径”下，Visa 在样本内（Visa、American Express、Diners Club/Discover、JCB、Mastercard）Payments Volume、Total Volume、Total Transactions、Cards 四项规模均为第一，Mastercard 为第二梯队，其余网络在该口径下规模显著更小。
- 同一对比表中，竞争对手数据注明来源与口径差异（例如第三方报告来源、是否包含特定网络/产品线、部分数据为估计），用于横向阅读时需同步考虑可比性边界。

### 竞争对手分析

#### **Mastercard**：

- 定位与竞争关系：被归入“Global or Multi-regional Networks”的主要样本之一，属于与 Visa 在多区域范围内直接竞争的卡组织网络。
- 规模对比（calendar year 2024，对比表口径）：
  - Payments Volume：8,014（$B）
  - Total Volume：9,757（$B）
  - Total Transactions：204（B）
  - Cards：3,146（M）
- 口径提示：对比表脚注对 Mastercard 数据范围与排除项作了说明（例如不含部分网络/产品线），横向比较需以脚注口径为边界。

#### **American Express**：

- 定位与竞争关系：被归入“Global or Multi-regional Networks”的主要样本之一，属于与 Visa 争夺消费者支付与机构/商户参与的竞争对手。
- 规模对比（calendar year 2024，对比表口径）：
  - Payments Volume：1,750（$B）
  - Total Volume：1,765（$B）
  - Total Transactions：12（B）
  - Cards：147（M）
- 口径提示：对比表脚注对 American Express 的数据覆盖范围作了说明（含商业/小微等口径与第三方发卡相关口径），用于对比时需结合脚注理解。

#### **JCB**：

- 定位与竞争关系：被归入“Global or Multi-regional Networks”的样本之一，并被提示可能在特定地理区域更为集中（示例包括日本）。
- 规模对比（calendar year 2024，对比表口径）：
  - Payments Volume：319（$B）
  - Total Volume：327（$B）
  - Total Transactions：7（B）
  - Cards：167（M）
- 口径提示：对比表脚注提示 JCB 相关口径中包含“其他支付相关产品”且部分数据为估计值，横向对比应以脚注口径为边界。

### 同业对比分析

#### **市场份额对比**：

- 【分析】样本内规模占比（按对比表口径计算；不代表全市场“份额”）：
  - Payments Volume（$B）占比：Visa 56.5%，Mastercard 33.7%，American Express 7.4%，JCB 1.3%，Diners Club/Discover 1.1%
  - Total Volume（$B）占比：Visa 56.8%，Mastercard 34.8%，American Express 6.3%，JCB 1.2%，Diners Club/Discover 0.9%
  - Total Transactions（B）占比：Visa 57.8%，Mastercard 37.9%，American Express 2.2%，JCB 1.3%，Diners Club/Discover 0.7%
  - Cards（M）占比：Visa 57.6%，Mastercard 37.7%，JCB 2.0%，American Express 1.8%，Diners Club/Discover 0.9%
- 【分析】上述占比仅覆盖对比表所列网络样本，且受脚注所述“统计口径/排除项/估计值”影响；不能直接外推至包含本地网络、RTP、数字钱包、替代支付等在内的全量竞争边界。

#### **毛利率对比**：

- 【占位符】
  - 缺口：同业口径下的“毛利率”可比定义与同业数据（至少需要竞争对手财报口径一致的收入/成本定义）；当前材料范围仅包含 Visa 自身披露与网络规模对比表，无法形成同业毛利率对比。
  - 需要：竞争对手年度/季度财报中的收入与成本披露口径（或同一监管披露中提供的同口径对比），并明确“毛利/成本”在支付网络业务中的可比科目映射。
  - 已检索范围：Visa | Form 10-K（FY2025）| Item 8 财务报表（损益表展示为 net revenue 与 operating expenses 结构）；Item 1 竞争部分的网络规模对比表。
  - 下一步：若允许扩展来源范围，补充竞争对手监管披露后再按统一科目映射计算并对比。

#### **运营利润率对比**：

- Visa 运营利润率（Operating income / Net revenue；单位：$ millions，FY 口径）：
  - FY2025：23,994 / 40,000 ≈ 60.0%
  - FY2024：23,595 / 35,926 ≈ 65.7%
  - FY2023：21,000 / 32,653 ≈ 64.3%
- 【占位符】
  - 缺口：同业（竞争对手）运营利润率数据与可比口径；当前材料范围未包含竞争对手财务报表披露。
  - 需要：竞争对手同期间损益表（或监管披露中同口径可比指标），并明确口径（如是否按净收入/总收入、是否包含特定网络/业务线）。
  - 已检索范围：Visa | Form 10-K（FY2025）| Item 8（Consolidated Statements of Operations）。
  - 下一步：若允许扩展来源范围，补充竞争对手披露后再做同口径对比。

#### **归母净利润率对比**：

- Visa 净利润率（Net income / Net revenue；单位：$ millions，FY 口径）：
  - FY2025：20,058 / 40,000 ≈ 50.1%
  - FY2024：19,743 / 35,926 ≈ 54.9%
  - FY2023：17,273 / 32,653 ≈ 52.9%
- 【占位符】
  - 缺口：同业（竞争对手）“归母净利润率”同口径对比；当前材料范围未包含竞争对手净利润披露。
  - 需要：竞争对手同期间净利润（归属口径）与收入口径的对应关系说明，以保证分子分母一致。
  - 已检索范围：Visa | Form 10-K（FY2025）| Item 8（Consolidated Statements of Operations）。
  - 下一步：若允许扩展来源范围，补充竞争对手披露后再做同口径对比。

### 证据与出处

- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1. Business | Competition（竞争对手类别划分、calendar year 2024 网络对比表及脚注口径与数据来源说明）
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 8. Financial Statements and Supplementary Data | Consolidated Statements of Operations（FY2023–FY2025：net revenue、operating income、net income）

## 风险分析

### 结论要点

- 【分析】本章风险要点围绕监管与税务、诉讼与调查、竞争与生态伙伴关系、宏观与地缘政治等外部冲击、结算赔付与流动性、技术迭代与网络安全、并购整合与人才、以及治理与资本结构等维度展开。
- 【前瞻】若全球监管规则、执法环境或税法发生变化，合规成本与不确定性可能上升，并可能对经营与财务结果造成不利影响。
- 【分析】公司将行业竞争与卖方/处理商降低受理成本、挑战行业实践等因素列为重要风险来源，相关变化可能对业务造成压力。
- 【前瞻】技术变迁与网络/系统中断或网络事件可能扰动业务连续性并损害经营结果；结算相关赔付义务可能带来重大损失风险并影响流动性。

### 详细情况

- 【前瞻】监管与合规：处于复杂且持续变化的全球监管环境之下，监管要求变化、执法与合规约束可能对业务与财务结果造成不利影响。
- 【前瞻】税务：税务检查/争议或税法变化可能带来成本与不确定性。
- 【前瞻】诉讼与调查：诉讼或调查的结果可能对经营、财务状况或声誉造成不利影响。
- 【分析】竞争：公司在风险因素中将行业竞争描述为激烈；竞争格局变化可能对业务造成不利影响。
- 【前瞻】客户与卖方基础：净收入与利润依赖客户与卖方基础；赢得、留存与发展相关基础可能需要较高成本并影响经营结果。
- 【前瞻】生态伙伴依赖：业务依赖与金融机构、收单机构、处理商、卖方、支付服务商、支付促进商、电商平台、金融科技公司及其他第三方的关系；关键关系变化可能损害业务。
- 【前瞻】受理成本压力：卖方与处理商持续推动降低受理成本、并挑战行业实践的行为可能损害业务。
- 【前瞻】宏观与外部事件：全球经济、政治、市场、健康与社会事件或环境变化可能损害业务。
- 【前瞻】结算赔付与流动性：对客户结算损失的赔付（indemnification）义务使公司暴露于重大损失风险，并可能降低流动性。
- 【前瞻】技术迭代：未能预见、适应或跟上支付行业新技术可能损害业务并影响未来增长。
- 【前瞻】技术与网络安全：网络或系统中断、故障或被攻破（包括由网络事件或攻击引发）可能损害业务。
- 【前瞻】并购/合营/投资：可能无法实现收购、合营或战略投资的预期收益，并可能因此面临风险与不确定性。
- 【前瞻】人才与组织：可能无法吸引、招聘与留住高素质员工（包括关键管理层）。
- 【前瞻】治理与资本结构：不同类别普通股与优先股持有人在重大交易上的利益可能与A类普通股股东不同；特拉华州法律、公司章程/细则及资本结构可能增加并购、收购或控制权变更难度。

### 证据与出处

- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1A. Risk Factors | We are subject to complex and evolving global regulations that could harm our business and financial results.
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1A. Risk Factors | We may be subject to tax examinations or disputes, or changes in tax laws.
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1A. Risk Factors | We may be adversely affected by the outcome of litigation or investigations.
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1A. Risk Factors | We face intense competition in our industry.
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1A. Risk Factors | Our net revenue and profits are dependent on our client and seller base, which may be costly to win, retain and develop.
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1A. Risk Factors | Sellers’ and processors’ continued push to lower acceptance costs and challenge industry practices could harm our business.
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1A. Risk Factors | We depend on relationships with financial institutions, acquirers, processors, sellers, payment facilitators, ecommerce platforms, fintechs and other third parties.
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1A. Risk Factors | Global economic, political, market, health and social events or conditions may harm our business.
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1A. Risk Factors | Our indemnification obligation to fund settlement losses of our clients exposes us to significant risk of loss and may reduce our liquidity.
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1A. Risk Factors | Failure to anticipate, adapt to, or keep pace with, new technologies in the payments industry could harm our business and impact future growth.
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1A. Risk Factors | A disruption, failure or breach of our networks or systems, including as a result of cyber incidents or attacks, could harm our business.
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1A. Risk Factors | We may not achieve the anticipated benefits of our acquisitions, joint ventures or strategic investments, and may face risks and uncertainties as a result.
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1A. Risk Factors | We may be unable to attract, hire and retain a highly qualified workforce, including key management.
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1A. Risk Factors | Holders of our class B-1, B-2 and C common stock and series A, B and C preferred stock may have different interests than our class A common shareholders concerning certain significant transactions.
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089 | Item 1A. Risk Factors | Delaware law, provisions in our certificate of incorporation and bylaws, and our capital structure could make a merger, takeover attempt or change in control difficult.

---

## 来源清单

- SEC EDGAR | Form DEF 14A | Filed 2025-12-08 | Accession 0001308179-25-000635
- SEC EDGAR | Form 10-K | Filed 2025-11-06 | Accession 0001403161-25-000089
- SEC EDGAR | Form 10-K | Filed 2024-11-13 | Accession 0001403161-24-000058
- SEC EDGAR | Form 10-K | Filed 2023-11-15 | Accession 0001403161-23-000099
- SEC EDGAR | Form 10-K | Filed 2022-11-16 | Accession 0001403161-22-000081
- SEC EDGAR | Form 10-K | Filed 2021-11-18 | Accession 0001403161-21-000060
- SEC EDGAR | Form 10-K | Filed 2020-11-19 | Accession 0001403161-20-000070
- SEC EDGAR | Form 10-K | Filed 2016-11-15 | Accession 0001403161-16-000058
- SEC EDGAR | Form 10-K | Filed 2008-11-21 | Accession 0001193125-08-240384
- SEC EDGAR | Form 10-K | Filed 2007-12-21 | Accession 0001193125-07-270394

**免责声明**

*本文内容是基于当前信息撰写，不保证该等信息的准确性和完整性。本文所载的资料、工具、意见及推测只提供给本文所针对的客户对象作参考之用，在任何情况下并不视为或被视为投资操作的建议。历史业绩不代表未来，产品有风险，投资需谨慎。在任何情况下本公司/本人不对任何人因使用本文中的任何内容所引致的任何损失承担任何责任。未经书面许可，任何机构和个人不得以任何形式翻版、复制、发表或引用。如征得本公司/本人同意进行引用、刊发的，需在允许的范围内使用，并注明出处，且不得对本文进行任何有悖原意的引用、删节和修改。本文内容仅用作沟通交流之用，不构成任何投资建议、交易依据、法律或税务意见。*
