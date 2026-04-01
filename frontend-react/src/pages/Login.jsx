import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Form, Input, Button, message, Card } from 'antd'
import { UserOutlined, LockOutlined, MedicineBoxOutlined } from '@ant-design/icons'

export default function Login({ onLogin }) {
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleLogin = async (values) => {
    setLoading(true)
    setTimeout(() => {
      if (values.username && values.password) {
        message.success('登录成功')
        onLogin()
        navigate('/')
      } else {
        message.error('请输入用户名和密码')
      }
      setLoading(false)
    }, 500)
  }

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #165DFF 0%, #36CFC9 100%)',
      }}
    >
      <Card
        style={{
          width: 400,
          borderRadius: 16,
          boxShadow: '0 8px 32px rgba(0,0,0,0.2)',
        }}
      >
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <div
            style={{
              width: 64,
              height: 64,
              borderRadius: 16,
              background: 'linear-gradient(135deg, #165DFF 0%, #36CFC9 100%)',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: 16,
            }}
          >
            <MedicineBoxOutlined style={{ fontSize: 32, color: 'white' }} />
          </div>
          <h1 style={{ fontSize: 24, fontWeight: 600, color: '#1E293B', margin: 0 }}>
            智肤康
          </h1>
          <p style={{ color: '#64748B', marginTop: 8 }}>
            皮肤疾病AI全流程辅助诊疗系统
          </p>
        </div>

        <Form
          name="login"
          onFinish={handleLogin}
          size="large"
        >
          <Form.Item
            name="username"
            rules={[{ required: true, message: '请输入用户名' }]}
          >
            <Input
              prefix={<UserOutlined style={{ color: '#94A3B8' }} />}
              placeholder="用户名"
            />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[{ required: true, message: '请输入密码' }]}
          >
            <Input.Password
              prefix={<LockOutlined style={{ color: '#94A3B8' }} />}
              placeholder="密码"
            />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              block
              style={{
                height: 44,
                background: 'linear-gradient(135deg, #165DFF 0%, #36CFC9 100%)',
                border: 'none',
                fontWeight: 600,
              }}
            >
              登录
            </Button>
          </Form.Item>
        </Form>

        <div style={{ textAlign: 'center', color: '#94A3B8', fontSize: 13 }}>
          <span>默认账号: admin / admin123</span>
        </div>
      </Card>
    </div>
  )
}
