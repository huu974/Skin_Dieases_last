import { Card, Typography, Row, Col, Statistic, Table, Tag, Button, Space, Empty } from 'antd'
import { DeleteOutlined, ExportOutlined, MedicineBoxOutlined } from '@ant-design/icons'
import React from 'react'

const { Title, Text } = Typography

const mockRecords = [
  { id: 1, image_name: 'skin_001.jpg', disease: '银屑病', disease_en: 'Psoriasis', confidence: 0.87, timestamp: '2026-03-28 10:30:00' },
  { id: 2, image_name: 'skin_002.jpg', disease: '湿疹', disease_en: 'Eczema', confidence: 0.76, timestamp: '2026-03-27 15:20:00' },
  { id: 3, image_name: 'skin_003.jpg', disease: '痤疮', disease_en: 'Acne', confidence: 0.92, timestamp: '2026-03-26 09:15:00' },
  { id: 4, image_name: 'skin_004.jpg', disease: '荨麻疹', disease_en: 'Urticaria', confidence: 0.68, timestamp: '2026-03-25 14:45:00' },
]

export default function History() {
  const records = mockRecords

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 60,
    },
    {
      title: '图像',
      dataIndex: 'image_name',
      key: 'image_name',
      render: (text) => <MedicineBoxOutlined style={{ fontSize: 24, color: '#165DFF' }} />,
      width: 80,
    },
    {
      title: '疾病名称',
      dataIndex: 'disease',
      key: 'disease',
      render: (text, record) => (
        <div>
          <Text strong>{text}</Text>
          <br />
          <Text type="secondary" style={{ fontSize: 12 }}>{record.disease_en}</Text>
        </div>
      ),
    },
    {
      title: '置信度',
      dataIndex: 'confidence',
      key: 'confidence',
      render: (conf) => (
        <Tag color={conf >= 0.8 ? 'green' : conf >= 0.6 ? 'orange' : 'red'}>
          {(conf * 100).toFixed(1)}%
        </Tag>
      ),
      width: 100,
    },
    {
      title: '诊断时间',
      dataIndex: 'timestamp',
      key: 'timestamp',
    },
    {
      title: '操作',
      key: 'action',
      render: () => (
        <Space>
          <Button type="text" icon={<ExportOutlined />}>导出</Button>
          <Button type="text" danger icon={<DeleteOutlined />}>删除</Button>
        </Space>
      ),
      width: 150,
    },
  ]

  const avgConfidence = records.length > 0
    ? (records.reduce((sum, r) => sum + r.confidence, 0) / records.length * 100).toFixed(1)
    : 0

  return (
    <div>
      <Title level={2} style={{ margin: 0 }}>
        诊断历史
      </Title>
      <Text type="secondary">查看和管理您的历史诊断记录</Text>

      <Row gutter={[16, 16]} style={{ marginTop: 24 }}>
        <Col xs={24} sm={8}>
          <Card>
            <Statistic
              title="总诊断次数"
              value={records.length}
              prefix={<MedicineBoxOutlined />}
              valueStyle={{ color: '#165DFF' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card>
            <Statistic
              title="最近诊断"
              value={records[0]?.timestamp || '暂无'}
              valueStyle={{ fontSize: 16 }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card>
            <Statistic
              title="平均置信度"
              value={avgConfidence}
              suffix="%"
              valueStyle={{ color: '#36CFC9' }}
            />
          </Card>
        </Col>
      </Row>

      <Card style={{ marginTop: 24 }}>
        {records.length > 0 ? (
          <Table
            columns={columns}
            dataSource={records}
            rowKey="id"
            pagination={{ pageSize: 5 }}
          />
        ) : (
          <Empty description="暂无诊断记录" />
        )}
      </Card>
    </div>
  )
}
