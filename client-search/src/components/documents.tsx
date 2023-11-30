'use client';

import {useState} from "react";
import {Button, FloatButton, Form, Input, List, message, Modal, Table} from "antd";
import axios from "axios";
import {PlusCircleOutlined, SearchOutlined} from "@ant-design/icons";

interface ListProps {
    dataList :any;
}
const MyListComponent = (props:ListProps) => {
    const {dataList} = props
    return (
        <List
            itemLayout="horizontal"
            dataSource={dataList}
            renderItem={(item:{title:string,content:string}) => (
                <List.Item>
                    <List.Item.Meta
                        title={item.title}
                        description={item.content}
                    />
                </List.Item>
            )}
        />
    );
};

export const DocumentPage = () => {
    const [searchText, setSearchText] = useState<string>('');
    const [dataSource, setDataSource] = useState<any>([]);
    const [isModalVisible, setIsModalVisible] = useState(false);

    const handleSearch = (value:string ) => {
        // Implement your search logic here
        // You can filter the dataSource based on the search text
        setSearchText(value);


        try {
            // Make an HTTP POST request to your backend API
             axios.get('http://localhost:5000/search', {params : {text : value,threshold:0.9 }})
                 .then((response => {
                 // Update the dataSource with the search results
                 setDataSource(response.data["docs"]);
             }));


          } catch (error) {
            console.error(error);
            // Handle error
          }
    };

    const handleInsert = () => {
        setIsModalVisible(true);
    };

    const handleOk = (values:any) => {
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

        <div style={{ padding: '20px',alignItems:"center" }}>
            <h1 style={{ marginBottom: '20px' }}>היוזמות לטיפול</h1>
            <div style={{ marginBottom: '16px' }}>
                <Input.Search
                    size={'large'}
                    style={{width : 500}}
                    placeholder="Search documents"
                    onSearch={handleSearch}
                    enterButton
                />

            </div>

            <MyListComponent dataList={dataSource}></MyListComponent>


            <Modal
                title="Insert Document"
                open={isModalVisible}
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
            <FloatButton icon={<PlusCircleOutlined />} onClick={handleInsert} type="primary" style={{ right: 24 }} />
        </div>


    );
};