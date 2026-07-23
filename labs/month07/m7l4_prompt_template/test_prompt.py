# Month7 L4：结构化提示模板  （对应 docs/07-llm-systems/prompting-basics.mdx）
# 目标：结构化提示契约——可填变量、可加 few-shot、可规定输出格式
# 用法：python labs/month07/m7l4_prompt_template/test_prompt.py


class PromptTemplate:
    def __init__(self, template, output_format=None, examples=None):
        self.template = template
        self.output_format = output_format
        self.examples = examples or []

    def render(self, **variables):
        parts = []
        for src, dst in self.examples:
            parts.append(f"示例: 输入={src} 输出={dst}")     # few-shot
        parts.append(self.template.format(**variables))     # 填变量
        if self.output_format:
            parts.append(f"输出格式: {self.output_format}")  # 规定格式
        return "\n".join(parts)


def run():
    t = PromptTemplate(
        "把这句翻译成英文: {text}",
        output_format="仅返回 JSON {en:...}",
        examples=[("你好", "hello")],
    )
    out = t.render(text="早上好")
    assert "早上好" in out and "hello" in out and "输出格式" in out
    print("✅ 全部通过: 结构化提示模板（变量/few-shot/输出格式）")


if __name__ == "__main__":
    run()
