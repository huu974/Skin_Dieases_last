import { useState } from 'react'
import { Card, Input, Button, Typography, Space, List, Avatar } from 'antd'
import { SendOutlined, DeleteOutlined, RobotOutlined, UserOutlined } from '@ant-design/icons'

const { Title, Text } = Typography
const { TextArea } = Input

const quickQuestions = [
  '脸上长痘痘怎么办？',
  '湿疹怎么护理？',
  '银屑病有哪些症状？',
  '荨麻疹怎么引起的？',
]

const quickResponses = {
  "脸上长痘痘怎么办？": `关于痤疮（青春痘）：

**常见原因：**
- 皮脂分泌旺盛，毛孔堵塞
- 细菌感染
- 激素水平变化

**护理建议：**
1. 每天用温和的洁面产品清洁面部2次
2. 不要用手挤压痘痘，以免留下疤痕
3. 选择非致痘的护肤品
4. 规律作息，减少熬夜

**饮食建议：**
- 少吃辛辣、油腻、甜食
- 多吃蔬菜水果

⚠️ 如痘痘严重或持续不退，建议就医皮肤科。`,

  "湿疹怎么护理？": `关于湿疹：

**常见症状：**
- 皮肤红斑、丘疹
- 剧烈瘙痒
- 皮肤干燥、脱屑

**护理建议：**
1. 保持皮肤湿润，使用保湿霜
2. 避免过热的水洗澡
3. 穿棉质宽松衣物
4. 避免抓挠患处

⚠️ 建议就医确诊类型并接受针对性治疗。`,

  "银屑病有哪些症状？": `关于银屑病（牛皮癣）：

**典型特征：**
- 红色斑块覆盖银白色鳞屑
- 薄膜现象（刮除鳞屑后可见薄膜）
- 点状出血
- 好发于头皮、肘部、膝盖

**诱发因素：**
- 感染
- 精神压力
- 外伤
- 吸烟、饮酒

⚠️ 请到正规医院皮肤科就诊。`,

  "荨麻疹怎么引起的？": `关于荨麻疹（风团）：

**典型特征：**
- 红色或苍白色风团
- 剧烈瘙痒
- 来去迅速（24小时内消退）

**常见诱因：**
- 食物过敏（海鲜、坚果等）
- 药物过敏
- 感染
- 物理刺激（冷、热、压力）

⚠️ 如出现呼吸困难，请立即就医！`,
}

export default function Chat() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: '🏥 您好！我是皮肤病智能诊断助手。请描述您遇到的皮肤问题？' },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSend = () => {
    if (!input.trim()) return

    const userMsg = { role: 'user', content: input }
    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setLoading(true)

    setTimeout(() => {
      const response = `感谢您的咨询！

根据您描述的：${input}

**一般性建议：**
1. 保持患处清洁干燥
2. 避免使用刺激性护肤品
3. 观察症状变化
4. 如有加重及时就医

⚠️ 本回答仅供参考，不作为正式医疗诊断。如症状持续或加重，请尽快就医。`

      setMessages((prev) => [...prev, { role: 'assistant', content: response }])
      setLoading(false)
    }, 1000)
  }

  const handleQuickQuestion = (q) => {
    setMessages([{ role: 'user', content: q }, { role: 'assistant', content: quickResponses[q] || '建议咨询专业医生。' }])
  }

  const handleClear = () => {
    setMessages([{ role: 'assistant', content: '🏥 您好！我是皮肤病智能诊断助手。请描述您遇到的皮肤问题？' }])
  }

  return (
    <div>
      <Title level={2} style={{ margin: 0 }}>
        智能对话
      </Title>
      <Text type="secondary">基于RAG知识库与大语言模型的AI医生助手</Text>

      <Space direction="vertical" size={16} style={{ width: '100%', marginTop: 16 }}>
        <Space wrap>
          {quickQuestions.map((q, i) => (
            <Button key={i} onClick={() => handleQuickQuestion(q)}>
              {q}
            </Button>
          ))}
        </Space>

        <Card
          bodyStyle={{
            padding: 0,
            height: 'calc(100vh - 380px)',
            overflowY: 'auto',
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <div style={{ flex: 1, padding: 16, overflowY: 'auto' }}>
            {messages.map((msg, index) => (
              <div
                key={index}
                style={{
                  display: 'flex',
                  justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
                  marginBottom: 12,
                }}
              >
                <div
                  style={{
                    maxWidth: '80%',
                    display: 'flex',
                    flexDirection: 'row-reverse',
                    alignItems: 'flex-start',
                    gap: 8,
                  }}
                >
                  <Avatar
                    icon={msg.role === 'user' ? <UserOutlined /> : <RobotOutlined />}
                    style={{
                      backgroundColor: msg.role === 'user' ? '#165DFF' : '#36CFC9',
                    }}
                  />
                  <div
                    style={{
                      background: msg.role === 'user' ? '#165DFF' : '#F8FAFC',
                      color: msg.role === 'user' ? 'white' : '#1E293B',
                      padding: '12px 16px',
                      borderRadius: msg.role === 'user' ? '18px 18px 4px 18px' : '18px 18px 18px 4px',
                      border: msg.role === 'user' ? 'none' : '1px solid #E2E8F0',
                    }}
                  >
                    <Text strong style={{ color: msg.role === 'user' ? 'white' : '#165DFF' }}>
                      {msg.role === 'user' ? '您' : 'AI医生'}
                    </Text>
                    <div style={{ whiteSpace: 'pre-wrap', marginTop: 4 }}>
                      {msg.content}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card bodyStyle={{ padding: 12 }}>
          <Space.Compact style={{ width: '100%' }}>
            <TextArea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onPressEnter={(e) => {
                if (!e.shiftKey) {
                  e.preventDefault()
                  handleSend()
                }
              }}
              placeholder="请描述您的皮肤问题..."
              autoSize={{ minRows: 1, maxRows: 4 }}
              style={{ borderRadius: '8px 0 0 8px' }}
            />
            <Button
              type="primary"
              icon={<SendOutlined />}
              onClick={handleSend}
              loading={loading}
              style={{
                background: 'linear-gradient(135deg, #165DFF 0%, #36CFC9 100%)',
                border: 'none',
                borderRadius: '0 8px 8px 0',
              }}
            >
              发送
            </Button>
          </Space.Compact>
          <Button
            type="text"
            icon={<DeleteOutlined />}
            onClick={handleClear}
            style={{ marginTop: 8 }}
          >
            🗑️ 清空对话
          </Button>
        </Card>
      </Space>
    </div>
  )
}
