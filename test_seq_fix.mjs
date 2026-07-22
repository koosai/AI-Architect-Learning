import { JSDOM } from 'jsdom';

const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>');
globalThis.window = dom.window;
globalThis.document = dom.window.document;
globalThis.Option = dom.window.Option;
globalThis.Image = dom.window.Image;

const mermaidModule = await import('mermaid');
const mermaid = mermaidModule.default;
mermaid.initialize({ startOnLoad: false });

const testCode = `sequenceDiagram
  autonumber
  actor Client as 触发客户端 (Client)
  participant Center as 通知中心 (NotificationCenter)
  
  box "装饰器套娃调用链 (WithRetry → WithMask → EmailSender)"
    participant Retry as 重试装饰器 (WithRetry)
    participant Mask as 脱敏装饰器 (WithMask)
    participant Email as 邮件发送器 (EmailSender)
  end

  Client->>Center: emit('order', '密码123')
  activate Center
  
  Note over Center: 遍历 'order' 订阅者列表
  
  Center->>Retry: send('密码123')
  activate Retry
  
  Retry->>Mask: 递归委托: send('密码123')
  activate Mask
  
  Note over Mask: (脱敏前置处理)<br/>'密码123' → '***123'
  
  Mask->>Email: 递归委托: send('***123')
  activate Email
  Email-->>Mask: 返回 'EMAIL: ***123'
  deactivate Email
  
  Mask-->>Retry: 返回 'EMAIL: ***123'
  deactivate Mask
  
  Note over Retry: (重试后置处理)<br/>如果失败可重试，成功则加上重试头标记
  
  Retry-->>Center: 返回 '(retry x2) EMAIL: ***123'
  deactivate Retry
  
  Center-->>Client: 返回所有订阅通道的发送结果
  deactivate Center`;

try {
  await mermaid.parse(testCode);
  console.log('SUCCESS! PASSES MERMAID.PARSE 100%!');
} catch (e) {
  console.log('FAIL:', e.message);
}
