import React, { useState } from 'react';
import { Input, Button, Table, Modal, Form, message } from 'antd';
import 'antd/dist/reset.css';


export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
     <DocumentPage />
    </main>
  )
}

const DocumentPage = () => {
  const [searchText, setSearchText] = useState('');
  const [dataSource, setDataSource] = useState([]);
  const [isModalVisible, setIsModalVisible] = useState(false);

  const columns = [
    {
      title: 'Document ID',
      dataIndex: 'id',
      key: 'id',
    },
    {
      title: 'Title',
      dataIndex: 'title',
      key: 'title',
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: 'Location',
      dataIndex: 'location',
      key: 'location',
    },
    {
      title: 'Contact Info',
      dataIndex: 'contactInfo',
      key: 'contactInfo',
    },
  ];

  const handleSearch = (value) => {
    // Implement your search logic here
    // You can filter the dataSource based on the search text
    setSearchText(value);

    try {
        // Make an HTTP POST request to your backend API
        const response = await axios.get('http://localhost:8000/api/search', {params : {text : value }});
        
        // Update the dataSource with the search results
        setDataSource(response.data);
      } catch (error) {
        console.error(error);
        // Handle error
      }
  };

  const handleInsert = () => {
    setIsModalVisible(true);
  };

  const handleOk = (values) => {
    // Implement your insert logic here
    // Add a new document to the dataSource with the provided values
    setDataSource([...dataSource, { ...values, id: dataSource.length + 1 }]);
    setIsModalVisible(false);
    message.success('Document inserted successfully');
  };

  const handleCancel = () => {
    setIsModalVisible(false);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1 style={{ marginBottom: '20px' }}>היוזמות לטיפול</h1>

      <div style={{ marginBottom: '16px' }}>
        <Input.Search
          placeholder="Search documents"
          onSearch={handleSearch}
          enterButton
        />
        <Button type="primary" style={{ marginLeft: '16px' }} onClick={handleInsert}>
          Insert Document
        </Button>
      </div>

      <Table
        dataSource={dataSource}
        columns={columns}
        pagination={{ pageSize: 10 }}
        rowKey="id"
      />

      <Modal
        title="Insert Document"
        visible={isModalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
      >
        <Form
          name="insertDocumentForm"
          initialValues={{ remember: true }}
          onFinish={handleOk}
        >
          <Form.Item
            label="Title"
            name="title"
            rules={[{ required: true, message: 'Please enter the title' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Description"
            name="description"
            rules={[{ required: true, message: 'Please enter the description' }]}
          >
            <Input.TextArea />
          </Form.Item>

          <Form.Item
            label="Location"
            name="location"
            rules={[{ required: true, message: 'Please enter the location' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Contact Info"
            name="contactInfo"
            rules={[{ required: true, message: 'Please enter the contact info' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit">
              Submit
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};