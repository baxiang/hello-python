import { defineConfig } from 'vitepress'
import { existsSync, readFileSync, readdirSync, statSync } from 'fs'
import { basename, join, relative } from 'path'

const EXCLUDE_DIRS = [
  'node_modules',
  '.vitepress',
  'docs',
  '.git',
  '.claude',
  '.ruff_cache',
  '.vscode',
  '.pytest_cache',
  '__pycache__',
  'app',
  'tests',
  'venv',
  'env',
]
const EXCLUDE_FILES = ['AGENTS.md', 'CLAUDE.md', 'QWEN.md']
const ROOT = process.cwd()

const LABEL_OVERRIDES: Record<string, string> = {
  '00-Python学习大纲': '学习大纲',
  '01-基础入门篇': '基础入门',
  '02-核心编程篇': '核心编程',
  '03-高级语法篇': '高级语法',
  '04-Web开发篇': 'Web 开发',
  '05-机器学习篇': '机器学习',
  '06-神经网络与深度学习篇': '深度学习',
  '07-项目实战篇': '项目实战',
  '08-工程实践篇': '工程实践',
  '09-LangChain与LangGraph篇': 'LangChain 与 LangGraph',
  '附录': '附录',
}

type SidebarItem = {
  text: string
  link?: string
  collapsed?: boolean
  items?: SidebarItem[]
}

type Module = {
  dir: string
  text: string
  link: string
}

function stripOrder(name: string): string {
  return name
    .replace(/^\d{2}-/, '')
    .replace(/^Level-\d+-/, '')
    .replace(/^\d+\.\d+\s*/, '')
}

function humanize(name: string, keepHyphen = false): string {
  const text = stripOrder(name)
  if (keepHyphen) return text.trim()

  return text
    .replace(/-/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
}

function displayLabel(path: string, fallback: string, keepHyphen = false): string {
  const rel = relative(ROOT, path).replace(/\\/g, '/').replace(/\.md$/, '')
  return LABEL_OVERRIDES[rel] ?? humanize(fallback, keepHyphen)
}

function readTitle(file: string): string | undefined {
  if (!existsSync(file)) return undefined

  const content = readFileSync(file, 'utf-8')
  const match = content.match(/^#\s+(.+)$/m)
  return match?.[1]?.trim()
}

function getLabel(file: string): string {
  const title = readTitle(file)
  if (title) return title
  return displayLabel(file, basename(file, '.md'), true)
}

function mdLink(file: string): string {
  const rel = relative(ROOT, file).replace(/\\/g, '/').replace(/\.md$/, '')
  return `/${rel}`
}

function isExcludedFile(entry: string): boolean {
  return EXCLUDE_FILES.includes(entry) || entry.startsWith('.')
}

function isPythonProjectDir(dir: string): boolean {
  return existsSync(join(dir, 'pyproject.toml'))
}

function collectPythonProjectExcludes(dir: string): string[] {
  const patterns: string[] = []

  for (const entry of readdirSync(dir)) {
    if (EXCLUDE_DIRS.includes(entry) || isExcludedFile(entry)) continue

    const full = join(dir, entry)
    const stat = statSync(full)
    if (!stat.isDirectory()) continue

    if (isPythonProjectDir(full)) {
      const rel = relative(ROOT, full).replace(/\\/g, '/')
      patterns.push(`${rel}/**`)
      continue
    }

    patterns.push(...collectPythonProjectExcludes(full))
  }

  return patterns
}

function hasMarkdown(dir: string): boolean {
  if (isPythonProjectDir(dir)) return false

  for (const entry of readdirSync(dir)) {
    if (EXCLUDE_DIRS.includes(entry)) continue

    const full = join(dir, entry)
    const stat = statSync(full)
    if (stat.isDirectory() && hasMarkdown(full)) return true
    if (stat.isFile() && entry.endsWith('.md') && !isExcludedFile(entry)) return true
  }
  return false
}

function findEntryPage(dir: string): string | undefined {
  if (isPythonProjectDir(dir)) return undefined

  for (const name of ['README.md', 'index.md']) {
    const file = join(dir, name)
    if (existsSync(file)) return file
  }

  const entries = readdirSync(dir).sort()
  for (const entry of entries) {
    if (EXCLUDE_DIRS.includes(entry) || isExcludedFile(entry)) continue

    const full = join(dir, entry)
    const stat = statSync(full)
    if (stat.isFile() && entry.endsWith('.md')) return full
    if (stat.isDirectory()) {
      const nested = findEntryPage(full)
      if (nested) return nested
    }
  }
}

function collectItems(dir: string, skipReadme = false): SidebarItem[] {
  const items: SidebarItem[] = []

  for (const entry of readdirSync(dir).sort()) {
    if (EXCLUDE_DIRS.includes(entry) || isExcludedFile(entry)) continue

    const full = join(dir, entry)
    const stat = statSync(full)

    if (stat.isDirectory()) {
      if (isPythonProjectDir(full)) continue

      const children = collectItems(full, true)
      if (children.length > 0) {
        const entryPage = findEntryPage(full)
        items.push({
          text: displayLabel(full, entry, true),
          link: entryPage ? mdLink(entryPage) : undefined,
          collapsed: false,
          items: children,
        })
      }
      continue
    }

    if (!entry.endsWith('.md')) continue
    if (skipReadme && entry === 'README.md') continue

    items.push({
      text: entry === 'README.md' ? '章节概览' : getLabel(full),
      link: mdLink(full),
    })
  }

  return items
}

function discoverModules(): Module[] {
  const modules: Module[] = []

  for (const entry of readdirSync(ROOT).sort()) {
    if (EXCLUDE_DIRS.includes(entry) || isExcludedFile(entry)) continue
    if (entry === 'index.md' || entry === 'README.md') continue

    const full = join(ROOT, entry)
    const stat = statSync(full)

    if (stat.isDirectory()) {
      if (!hasMarkdown(full)) continue

      const entryPage = findEntryPage(full)
      if (entryPage) {
        modules.push({
          dir: entry,
          text: displayLabel(full, entry),
          link: mdLink(entryPage),
        })
      }
      continue
    }

    if (stat.isFile() && entry.endsWith('.md')) {
      modules.push({
        dir: entry,
        text: getLabel(full),
        link: mdLink(full),
      })
    }
  }

  return modules
}

function buildSidebar(): Record<string, SidebarItem[]> {
  const sidebar: Record<string, SidebarItem[]> = {}

  for (const mod of discoverModules()) {
    const full = join(ROOT, mod.dir)
    if (!statSync(full).isDirectory()) continue

    const items = collectItems(full)
    if (items.length === 0) continue

    sidebar[`/${mod.dir}/`] = [
      {
        text: mod.text,
        collapsed: false,
        items,
      },
    ]
  }

  return sidebar
}

const modules = discoverModules()
const pythonProjectExcludes = collectPythonProjectExcludes(ROOT)

export default defineConfig({
  srcDir: '.',
  srcExclude: [
    'AGENTS.md',
    'CLAUDE.md',
    'QWEN.md',
    'docs/**',
    '**/app/**',
    '**/tests/**',
    '**/.venv/**',
    '**/venv/**',
    '**/env/**',
    '**/__pycache__/**',
    ...pythonProjectExcludes,
  ],
  title: 'Hello Python',
  description: 'Python 全栈学习路线教程',
  lang: 'zh-CN',
  cleanUrls: true,
  lastUpdated: true,
  ignoreDeadLinks: true,

  markdown: {
    html: false,
    lineNumbers: true,
  },

  themeConfig: {
    logo: '/python.svg',

    search: {
      provider: 'local',
    },

    nav: [
      { text: '首页', link: '/' },
      ...modules.map((m) => ({ text: m.text, link: m.link })),
    ],

    sidebar: buildSidebar(),

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
})
