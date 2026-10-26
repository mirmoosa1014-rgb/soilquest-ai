import { defineConfig } from 'vite';
export default defineConfig({server:{host:'127.0.0.1',port:5104,proxy:{'/api':'http://127.0.0.1:8104'}}});
