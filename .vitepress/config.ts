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
      { text: '基础入门', link: '/1-basics/01-Python入门/01-Python简介' },
      { text: '核心编程', link: '/2-core/01-函数/01-函数基础' },
      { text: '高级语法', link: '/3-advanced/01-模块与包/01-模块基础' },
      { text: 'Web 开发', link: '/4-web/01-Web基础/01-HTTP协议基础' },
      { text: '机器学习', link: '/5-ml/01-基础概念/01-机器学习基础' },
      { text: '深度学习', link: '/6-deep-learning/01-神经网络基础/01-神经网络基础' },
      { text: '项目实战', link: '/7-projects/' },
      { text: '工程实践', link: '/8-engineering/项目管理/01-pip包管理器' },
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
