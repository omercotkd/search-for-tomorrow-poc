import { Input, Button, Table, Modal, Form, message } from 'antd';
import 'antd/dist/reset.css';

import {DocumentPage} from "@/compoments/documents";


export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
     <DocumentPage />
    </main>
  )
}
