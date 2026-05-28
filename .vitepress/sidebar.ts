import { generateSidebar } from 'vitepress-sidebar'

const EXCLUDE_PATTERNS = [
  '**/__pycache__/**', '**/.venv/**', '**/venv/**', '**/env/**',
  '**/.pytest_cache/**', '**/.ruff_cache/**',
  '**/python_basics/**', '**/basic_syntax/**', '**/string_demo/**',
  '**/data_structures/**', '**/functions_demo/**', '**/oop_demo/**',
  '**/exceptions_demo/**', '**/iterators_demo/**', '**/decorators_demo/**',
  '**/type_hints_demo/**', '**/modules_demo/**', '**/builtin_demo/**',
  '**/flask_demo/**', '**/fastapi_demo/**', '**/async_demo/**',
  '**/ml_basics/**', '**/deep_learning_demo/**',
  '**/code_quality/**', '**/dev_tips/**', '**/monitoring/**',
  '**/project_mgmt/**', '**/ai_chat_assistant/**',
  '**/app/**', '**/src/**', '**/core/**', '**/utils/**', '**/tests/**',
  '**/node_modules/**', '**/site-packages/**',
]

const SIDEBAR_OPTIONS = {
  useTitleFromFileHeading: true,
  collapsed: true,
  sortMenusByFrontmatterOrder: true,
  frontmatterOrderDefaultValue: 100,
  includeDotFiles: false,
  excludeByGlobPattern: EXCLUDE_PATTERNS,
}

export default generateSidebar([
  {
    documentRootPath: '/1-basics',
    scanStartPath: '',
    resolvePath: '/1-basics/',
    ...SIDEBAR_OPTIONS,
  },
  {
    documentRootPath: '/2-core',
    scanStartPath: '',
    resolvePath: '/2-core/',
    ...SIDEBAR_OPTIONS,
  },
  {
    documentRootPath: '/3-advanced',
    scanStartPath: '',
    resolvePath: '/3-advanced/',
    ...SIDEBAR_OPTIONS,
  },
  {
    documentRootPath: '/4-web',
    scanStartPath: '',
    resolvePath: '/4-web/',
    ...SIDEBAR_OPTIONS,
  },
  {
    documentRootPath: '/5-ml',
    scanStartPath: '',
    resolvePath: '/5-ml/',
    ...SIDEBAR_OPTIONS,
  },
  {
    documentRootPath: '/6-deep-learning',
    scanStartPath: '',
    resolvePath: '/6-deep-learning/',
    ...SIDEBAR_OPTIONS,
  },
  {
    documentRootPath: '/7-projects',
    scanStartPath: '',
    resolvePath: '/7-projects/',
    ...SIDEBAR_OPTIONS,
  },
  {
    documentRootPath: '/8-engineering',
    scanStartPath: '',
    resolvePath: '/8-engineering/',
    ...SIDEBAR_OPTIONS,
  },
  {
    documentRootPath: '/appendix',
    scanStartPath: '',
    resolvePath: '/appendix/',
    ...SIDEBAR_OPTIONS,
  },
])
