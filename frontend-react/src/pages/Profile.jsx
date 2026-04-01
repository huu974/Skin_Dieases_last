import { Card, Form, Input, Button, Tabs, Row, Col, InputNumber, Radio, Space, message, Statistic } from 'antd'
import { UserOutlined, SaveOutlined, DeleteOutlined, SettingOutlined, DatabaseOutlined } from '@ant-design/icons'

export default function Profile() {
  const [form] = Form.useForm()

  const handleSave = (values) => {
    message.success('信息已保存!')
  }

  const handleClearData = () => {
    message.success('数据已清空!')
  }

  return (
    <div>
      <UserOutlined style={{ fontSize: 24 }} />
      <div style={{ marginBottom: 16 }}>
        <h2 style={{ margin: 0 }}>用户中心</h2>
        <p style={{ color: '#64748B', margin: '4px 0 0 0' }}>管理您的个人信息和诊断偏好</p>
      </div>

      <Card>
        <Tabs
          defaultActiveKey="1"
          items={[
            {
              key: '1',
              label: (
                <span>
                  <UserOutlined />
                  基本信息
                </span>
              ),
              children: (
                <Form
                  form={form}
                  layout="vertical"
                  onFinish={handleSave}
                  initialValues={{
                    name: '访客用户',
                    email: 'user@example.com',
                    phone: '',
                    age: 25,
                  }}
                >
                  <Row gutter={16}>
                    <Col xs={24} md={12}>
                      <Form.Item
                        name="name"
                        label="昵称"
                        rules={[{ required: true, message: '请输入昵称' }]}
                      >
                        <Input placeholder="请输入昵称" />
                      </Form.Item>
                    </Col>
                    <Col xs={24} md={12}>
                      <Form.Item
                        name="email"
                        label="邮箱"
                        rules={[
                          { required: true, message: '请输入邮箱' },
                          { type: 'email', message: '请输入有效的邮箱地址' }
                        ]}
                      >
                        <Input placeholder="请输入邮箱" />
                      </Form.Item>
                    </Col>
                    <Col xs={24} md={12}>
                      <Form.Item
                        name="phone"
                        label="电话"
                      >
                        <Input placeholder="请输入电话" />
                      </Form.Item>
                    </Col>
                    <Col xs={24} md={12}>
                      <Form.Item
                        name="age"
                        label="年龄"
                      >
                        <InputNumber min={0} max={120} style={{ width: '100%' }} />
                      </Form.Item>
                    </Col>
                  </Row>
                  <Button type="primary" htmlType="submit" icon={<SaveOutlined />}>
                    💾 保存修改
                  </Button>
                </Form>
              ),
            },
            {
              key: '2',
              label: (
                <span>
                  <SettingOutlined />
                  偏好设置
                </span>
              ),
              children: (
                <Space direction="vertical" size={24} style={{ width: '100%' }}>
                  <div>
                    <h4>主题模式</h4>
                    <Radio.Group defaultValue="light">
                      <Radio value="light">☀️ 浅色模式</Radio>
                      <Radio value="dark">🌙 深色模式</Radio>
                    </Radio.Group>
                  </div>
                  <div>
                    <h4>语言设置</h4>
                    <Radio.Group defaultValue="zh">
                      <Radio value="zh">中文</Radio>
                      <Radio value="en">English</Radio>
                    </Radio.Group>
                  </div>
                  <Button type="primary" icon={<SaveOutlined />}>
                    ⚙️ 保存偏好
                  </Button>
                </Space>
              ),
            },
            {
              key: '3',
              label: (
                <span>
                  <DatabaseOutlined />
                  数据管理
                </span>
              ),
              children: (
                <Space direction="vertical" size={24} style={{ width: '100%' }}>
                  <Row gutter={16}>
                    <Col xs={24} sm={12}>
                      <Card>
                        <Statistic
                          title="诊断记录"
                          value={4}
                          prefix={<DatabaseOutlined />}
                          valueStyle={{ color: '#165DFF' }}
                        />
                      </Card>
                    </Col>
                    <Col xs={24} sm={12}>
                      <Card>
                        <Statistic
                          title="对话记录"
                          value={12}
                          prefix={<DatabaseOutlined />}
                          valueStyle={{ color: '#36CFC9' }}
                        />
                      </Card>
                    </Col>
                  </Row>
                  <Button danger icon={<DeleteOutlined />} onClick={handleClearData}>
                    🗑️ 清空数据
                  </Button>
                </Space>
              ),
            },
          ]}
        />
      </Card>
    </div>
  )
}
