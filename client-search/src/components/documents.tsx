'use client';

import {useState} from "react";
import {Button, FloatButton, Form, Input, List, message, Modal, Slider, Table} from "antd";
import axios from "axios";
import {PlusCircleOutlined, SearchOutlined} from "@ant-design/icons";
import TextArea from "antd/es/input/TextArea";

interface ListProps {
    dataList :any;
}

const MyListComponent = (props:ListProps) => {
    const {dataList} = props
    return (
        <List
            itemLayout="horizontal"
            dataSource={dataList}
            renderItem={(item:{title:string,content:string,dist:number}) => (
                <List.Item>

                    <List.Item.Meta
                        avatar={
                            // @ts-ignore
                            <div>{item.dist.toFixed(2) * 100 }%</div>
                        }
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
    const [threshold, setThreshold] = useState(0.9);

    const handleTextChange = (e) => {
        setSearchText(e.target.value);
    };

    const handleSearch = () => {
        // Implement your search logic here
        // You can filter the dataSource based on the search text

        try {
            // Make an HTTP POST request to your backend API
             axios.get('http://localhost:5000/search', {params : {text :searchText ,threshold:threshold }})
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


    const onChange = (newValue:number) => {
        setThreshold(newValue);
    };
    const marks = {
        0.8: '0.8',
        0.9: '0.9',
        0.95: '0.95'
    };

    return (

        <div style={{ padding: '20px',alignItems:"center" }}>
            <h1 style={{ marginBottom: '20px' }}>היוזמות לטיפול</h1>
            <div style={{ marginBottom: '16px' }}>

                <Input.TextArea
                    placeholder="Search documents"
                    style={{width : 500,height:200}}
                    rows={4}
                    value={searchText}
                    onChange={handleTextChange}
                />

                <Button icon={<SearchOutlined/>} type={"primary"} onClick={handleSearch}></Button>
            </div>
            <div>
                <Slider defaultValue={threshold}
                        style={{width:500}}
                        min={0.8}
                        max={0.95}
                        step={0.01}
                        marks={marks}
                        value={typeof threshold === 'number' ? threshold : 0}
                        onChange={onChange} />
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