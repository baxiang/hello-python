import { defineConfig } from 'vitepress'
import sidebar from './sidebar'

const isProduction = process.env.NODE_ENV === 'production' || process.argv.includes('build')

export default defineConfig({
  title: '从零开始系统学习 Python 编程',
  description: 'Python 全栈学习路线教程',
  lang: 'zh-CN',
  base: isProduction ? '/hello-python/' : '/',
  cleanUrls: true,
  lastUpdated: true,
  ignoreDeadLinks: true,

  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '基础入门', link: '/1-basics/' },
      { text: '核心编程', link: '/2-core/' },
      { text: '高级语法', link: '/3-advanced/' },
      { text: 'Web 开发', link: '/4-web/' },
      { text: '机器学习', link: '/5-ml/' },
      { text: '深度学习', link: '/6-deep-learning/' },
      { text: '项目实战', link: '/7-projects/' },
      { text: '工程实践', link: '/8-engineering/' },
      { text: 'LangChain', link: '/9-langchain/' },
    ],

    sidebar,

    search: {
      provider: 'local',
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/baxiang/hello-python' },
    ],

    outline: {
      label: '本页目录',
      level: [2, 3],
    },

    docFooter: {
      prev: '上一篇',
      next: '下一篇',
    },

    lastUpdated: {
      text: '最后更新',
      formatOptions: {
        dateStyle: 'medium',
        timeStyle: 'short',
      },
    },
  },

  markdown: {
    lineNumbers: true,
  },

  srcExclude: [
    '**/node_modules/**',
    '**/__pycache__/**',
    '**/.venv/**',
    '**/venv/**',
    '**/env/**',
    '**/.pytest_cache/**',
    '**/target/**',
    '**/.vitepress/**',
    '**/*_demo/**',
    '**/*_basics/**',
    '**/python_basics/**',
    '**/basic_syntax/**',
    '**/string_demo/**',
    '**/data_structures/**',
    '**/flask_demo/**',
    '**/fastapi_demo/**',
    '**/async_demo/**',
    '**/ml_basics/**',
    '**/langchain_basics/**',
    '**/langgraph_basics/**',
    '**/agent_basics/**',
    '**/langchain_advanced/**',
    '**/langgraph_advanced/**',
    '**/agent_assistant/**',
    '**/chatbot/**',
    '**/doc_qa/**',
    '**/multi_agent/**',
    '**/ai_chat_assistant/**',
    '**/code_quality/**',
    '**/dev_tips/**',
    '**/monitoring/**',
    '**/project_mgmt/**',
    'docs/**',
    'scripts/**',
    'AGENTS.md',
    'CLAUDE.md',
    '.github/**',
  ],
})
