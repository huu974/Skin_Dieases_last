import { Card, Row, Col, Statistic, Typography, Space } from 'antd'
import { useNavigate } from 'react-router-dom'
import {
  MedicineBoxOutlined,
  MessageOutlined,
  SafetyOutlined,
  HistoryOutlined,
  UserOutlined,
  ArrowUpOutlined,
} from '@ant-design/icons'

const { Title, Text, Paragraph } = Typography

const features = [
  {
    key: '/diagnosis',
    icon: <MedicineBoxOutlined style={{ fontSize: 32, color: '#165DFF' }} />,
    title: '诊断分析',
    desc: '上传皮肤图像，AI实时分析皮肤病症状',
    color: '#E8F4FF',
  },
  {
    key: '/chat',
    icon: <MessageOutlined style={{ fontSize: 32, color: '#36CFC9' }} />,
    title: '智能对话',
    desc: '与AI助手对话，详细描述您的症状',
    color: '#E8FFFE',
  },
  {
    key: '/prevention',
    icon: <SafetyOutlined style={{ fontSize: 32, color: '#0FC6C2' }} />,
    title: '预防建议',
    desc: '获取专业皮肤病预防和护理建议',
    color: '#E8FFF4',
  },
  {
    key: '/history',
    icon: <HistoryOutlined style={{ fontSize: 32, color: '#FF8C00' }} />,
    title: '历史记录',
    desc: '查看历史诊断记录和分析报告',
    color: '#FFF4E8',
  },
]

export default function Home() {
  const navigate = useNavigate()
  const navigateTo = (path) => {
    navigate(path)
  }

  return (
    <div style={{ padding: '0 0 24px 0' }}>
      <div
        style={{
          background: 'linear-gradient(135deg, #165DFF 0%, #36CFC9 100%)',
          borderRadius: 16,
          padding: '32px 32px 48px 32px',
          color: 'white',
          marginBottom: 24,
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <div style={{ position: 'relative', zIndex: 1 }}>
          <Title level={1} style={{ color: 'white', margin: 0, fontSize: 28 }}>
            欢迎使用智肤康
          </Title>
          <Paragraph style={{ color: 'rgba(255,255,255,0.85)', margin: '12px 0 0 0', fontSize: 15 }}>
            皮肤疾病AI全流程辅助诊疗系统
          </Paragraph>
        </div>
        <div
          style={{
            position: 'absolute',
            right: -50,
            top: -50,
            width: 200,
            height: 200,
            borderRadius: '50%',
            background: 'rgba(255,255,255,0.1)',
          }}
        />
      </div>

      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} lg={6}>
          <Card hoverable>
            <Statistic
              title="总诊断次数"
              value={156}
              prefix={<MedicineBoxOutlined />}
              valueStyle={{ color: '#165DFF' }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              <ArrowUpOutlined /> 较上周 +12%
            </Text>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card hoverable>
            <Statistic
              title="支持疾病类型"
              value={23}
              prefix={<SafetyOutlined />}
              valueStyle={{ color: '#36CFC9' }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              覆盖常见皮肤病
            </Text>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card hoverable>
            <Statistic
              title="诊断准确率"
              value={92.5}
              prefix={<UserOutlined />}
              suffix="%"
              valueStyle={{ color: '#0FC6C2' }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              基于HAM10000数据集
            </Text>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card hoverable>
            <Statistic
              title="用户总数"
              value={89}
              prefix={<UserOutlined />}
              valueStyle={{ color: '#FF8C00' }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              <ArrowUpOutlined /> 较上周 +5%
            </Text>
          </Card>
        </Col>
      </Row>

      <Title level={4} style={{ margin: '24px 0 16px 0' }}>
        核心功能
      </Title>
      <Row gutter={[16, 16]}>
        {features.map((item) => (
          <Col xs={24} sm={12} lg={6} key={item.key}>
            <Card
              hoverable
              onClick={() => navigateTo(item.key)}
              style={{ borderRadius: 12 }}
              bodyStyle={{ padding: 24 }}
            >
              <Space direction="vertical" size={12} style={{ width: '100%', textAlign: 'center' }}>
                <div
                  style={{
                    width: 64,
                    height: 64,
                    borderRadius: 16,
                    background: item.color,
                    display: 'inline-flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  {item.icon}
                </div>
                <div>
                  <Text strong style={{ fontSize: 16 }}>{item.title}</Text>
                  <br />
                  <Text type="secondary">{item.desc}</Text>
                </div>
              </Space>
            </Card>
          </Col>
        ))}
      </Row>

      <Title level={4} style={{ margin: '24px 0 16px 0' }}>
        支持的疾病类型
      </Title>
      <Card>
        <Row gutter={[8, 8]}>
          {[
            '痤疮与酒渣鼻', '光化性角化病', '特应性皮炎', '湿疹',
            '皮疹与药物反应', '疱疹/HPV', '色素性疾病', '狼疮',
            '黑色素瘤', '指甲疾病', '银屑病', '荨麻疹',
            '血管瘤', '血管炎', '疣/病毒感染', '真菌感染',
          ].map((disease) => (
            <Col xs={12} sm={8} md={6} lg={3} key={disease}>
              <div
                style={{
                  padding: '8px 12px',
                  background: '#F8FAFC',
                  borderRadius: 8,
                  textAlign: 'center',
                  fontSize: 13,
                }}
              >
                {disease}
              </div>
            </Col>
          ))}
        </Row>
      </Card>
    </div>
  )
}
