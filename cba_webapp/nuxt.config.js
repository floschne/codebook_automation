const proxyConfig = () => {
  let proxyTarget = ''

  if (process.env.CBA_DEPLOY === 'local') {
    proxyTarget = 'http://localhost:8081/'
  } else {
    const dockerApiHost = process.env.CBA_API_HOST
    const dockerApiPort = process.env.CBA_API_PORT

    proxyTarget = 'http://' + dockerApiHost + ':' + dockerApiPort + '/'
  }

  return {
    '/api/': { target: proxyTarget, pathRewrite: { '^/api/': '' } }
  }
}

export default {
  // Global page headers (https://go.nuxtjs.dev/config-head)
  head: {
    title: 'cba_webapp',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },

  // Global CSS (https://go.nuxtjs.dev/config-css)
  css: [],

  // Plugins to run before rendering page (https://go.nuxtjs.dev/config-plugins)
  plugins: [
    '@/plugins/generalApiClient.js',
    '@/plugins/datasetApiClient.js',
    '@/plugins/modelApiClient.js',
    '@/plugins/trainingApiClient.js',
    '@/plugins/predictionApiClient.js'
  ],

  // Auto import components (https://go.nuxtjs.dev/config-components)
  components: true,

  // Modules for dev and build (recommended) (https://go.nuxtjs.dev/config-modules)
  buildModules: [
    // https://go.nuxtjs.dev/eslint
    '@nuxtjs/eslint-module'
  ],

  // Modules (https://go.nuxtjs.dev/config-modules)
  modules: [
    // https://go.nuxtjs.dev/bootstrap
    'bootstrap-vue/nuxt',
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    '@nuxtjs/proxy',
    // https://www.npmjs.com/package/nuxt-highlightjs
    'nuxt-highlightjs'
  ],

  // https://github.com/nuxt-community/proxy-module#readme
  // needed for CORS
  proxy: proxyConfig(),

  // Axios module configuration (https://go.nuxtjs.dev/config-axios)
  axios: {
    proxy: true
  },

  // https://bootstrap-vue.org/docs#icons
  bootstrapVue: {
    icons: true // Install the IconsPlugin (in addition to BootStrapVue plugin
  },

  // Build Configuration (https://go.nuxtjs.dev/config-build)
  build: {},

  server: {
    port: 3000, // default: 3000
    host: '0.0.0.0', // default: localhost,
    timing: false
  },

  router: {
    base: process.env.CBA_CONTEXT_PATH
  }
}
