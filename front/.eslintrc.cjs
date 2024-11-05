module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
    es2020: true
  },
  extends: [
    "next/core-web-vitals",
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:tailwindcss/recommended",
    "prettier"
  ],
  parser: "@typescript-eslint/parser",
  plugins: [
    "import",
    "unused-imports",
    "@typescript-eslint",
    "react",
    "react-refresh"
  ],
  parserOptions: {
    project: "./tsconfig.json",
    tsconfigRootDir: __dirname
  },
  settings: {
    tailwindcss: {
      callees: ["cn", "classnames", "clsx", "ctl"], // These are the default values but feel free to customize
      config: "tailwind.config.js", // returned from `loadConfig()` utility if not provided
      cssFiles: [
        "**/*.css",
        "!**/node_modules",
        "!**/.*",
        "!**/dist",
        "!**/build"
      ],
      cssFilesRefreshRate: 5_000,
      removeDuplicates: true,
      skipClassAttribute: false,
      whitelist: ["((bg|text|animate)\\-).*", "markdown"],
      tags: [], // can be set to e.g. ['tw'] for use in tw`bg-blue`
      classRegex: "^class(Name)?$" // can be modified to support custom attributes. E.g. "^tw$" for `twin.macro`
    }
  },
  rules: {
    "@typescript-eslint/no-unused-vars": "off",
    "unused-imports/no-unused-imports": "warn",
    "import/order": [
      "warn",
      {
        groups: [
          "builtin",
          "external",
          "internal",
          "parent",
          "sibling",
          "index",
          "object",
          "type"
        ],
        "newlines-between": "always", // import groups の間を1行あける
        pathGroupsExcludedImportTypes: ["builtin"],
        alphabetize: {
          order: "asc", // 昇順
          caseInsensitive: true // 大文字小文字を区別する
        },
        pathGroups: [
          { pattern: "src/types/**", group: "internal", position: "before" },
          {
            pattern: "src/repositories/**",
            group: "internal",
            position: "before"
          }
        ]
      }
    ],
    "@typescript-eslint/consistent-type-imports": [
      "warn",
      {
        prefer: "type-imports"
      }
    ],
    "react-refresh/only-export-components": [
      "warn",
      {
        allowConstantExport: true
      }
    ],
    "react/no-unescaped-entities": "off",
    "react/jsx-uses-react": "off",
    "react/react-in-jsx-scope": "off",
    "react/jsx-sort-props": [
      "warn",
      {
        callbacksLast: false,
        shorthandFirst: true,
        ignoreCase: true,
        noSortAlphabetically: false,
        reservedFirst: true
      }
    ],
    "no-restricted-imports": [
      "error",
      {
        patterns: ["./styled-system/jsx/*", "@/styled-system/jsx/*"]
      }
    ]
  },
  overrides: [
    {
      files: ["**/*.tsx"],
      rules: {
        "react/prop-types": "off"
      }
    }
  ]
};
