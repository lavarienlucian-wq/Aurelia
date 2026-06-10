<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import heroImage from './assets/factory-hero.png'
import logoImage from './assets/logo.svg'

const routes = [
  { label: '首页', path: '/' },
  { label: '产品', path: '/products' },
  { label: '定制', path: '/custom' },
  { label: '工厂', path: '/factory' },
  { label: '联系', path: '/contact' },
]

const productLines = [
  {
    name: '客厅轻奢套系',
    material: '头层牛皮 / 高密海绵 / 镀钛金属',
    scope: '模块沙发、单椅、茶几、边几、电视柜',
    text: '以低饱和色彩和利落比例建立空间主调，适合门店陈列、样板间和高端公寓批量配套。',
  },
  {
    name: '餐厅成套套系',
    material: '黑胡桃木皮 / 岩板 / 微纤皮',
    scope: '餐桌、餐椅、餐边柜、酒柜',
    text: '桌椅柜统一线条、统一色板，兼顾日常耐用和接待场景的高级感。',
  },
  {
    name: '卧室收纳套系',
    material: '环保板材 / 实木贴皮 / 静音五金',
    scope: '床、床头柜、衣柜、梳妆台、斗柜',
    text: '从睡眠尺度、灯光氛围到收纳比例完整规划，适合精装房、民宿和品牌套房项目。',
  },
  {
    name: '全屋柜体系统',
    material: 'ENF 级板材 / 铝框玻璃 / 隐藏灯带',
    scope: '玄关、厨房、衣帽间、书房、展示柜',
    text: '工厂拆单、孔位预制、五金配套和包装编号统一管理，减少现场安装不确定性。',
  },
]

const materialLibrary = [
  '胡桃木、橡木、烟熏木皮与开放漆',
  '岩板、天然石纹、微水泥与金属饰面',
  '纳帕皮、科技布、绒面面料与工程阻燃面料',
  '铝框玻璃、隐藏拉手、静音铰链与高承重滑轨',
]

const customSteps = [
  {
    title: '需求建档',
    text: '收集空间图纸、产品清单、风格参考、预算区间和交付节点，建立项目档案。',
  },
  {
    title: '方案深化',
    text: '由设计、结构、工艺和报价团队共同评审尺寸、节点、材料和成本。',
  },
  {
    title: '样板确认',
    text: '提供色板、面料、五金、木皮和关键结构样板，必要时制作单品首样。',
  },
  {
    title: '排产制造',
    text: '按物料清单、工艺单和包装标准进入工厂排产，关键节点同步进度。',
  },
  {
    title: '质检交付',
    text: '完成外观、结构、尺寸、五金、包装检查，支持整车、零担和工程分批发运。',
  },
]

const factoryStats = [
  { value: '28,000m2', label: '现代化生产基地' },
  { value: '12+', label: '核心工艺工段' },
  { value: '72h', label: '常规打样响应' },
  { value: '100%', label: '出厂质检留档' },
]

const factorySections = [
  {
    title: '板式与柜体',
    text: '开料、封边、排孔、试装和拆单包装统一管理，适配全屋柜体和工程批量交付。',
  },
  {
    title: '软体与坐感',
    text: '沙发、床具、单椅支持多层海绵、羽绒、蛇簧和绷带结构组合，坐感可按渠道定位调整。',
  },
  {
    title: '木作与涂装',
    text: '木皮拼花、开放漆、哑光漆和金属饰面协同控制，确保不同品类之间色差更稳定。',
  },
  {
    title: '包装与发运',
    text: '按项目、楼栋、户型和安装顺序进行包装编号，降低终端仓储与安装沟通成本。',
  },
]

const projectTypes = ['品牌贴牌', '设计师项目', '工程批量', '门店上样', '全屋定制', '酒店/民宿']
const quantityOptions = ['1-10 件', '11-50 件', '51-200 件', '200 件以上', '整屋/整层项目']
const budgetOptions = ['10 万以内', '10-30 万', '30-80 万', '80-200 万', '200 万以上', '待评估']

const form = reactive({
  contactName: '',
  phone: '',
  company: '',
  projectType: '',
  quantity: '',
  city: '',
  budget: '',
  message: '',
})

const formSubmitted = ref(false)
const submittedContact = ref('')
const isSubmitting = ref(false)
const submitError = ref('')
const currentPath = ref(normalizePath(window.location.pathname))

function normalizePath(pathname) {
  const path = pathname.replace(/\/$/, '') || '/'
  return routes.some((route) => route.path === path) ? path : '/'
}

function goTo(path, event) {
  event.preventDefault()
  if (path !== currentPath.value) {
    window.history.pushState({}, '', path)
    currentPath.value = path
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

function syncPath() {
  currentPath.value = normalizePath(window.location.pathname)
}

async function submitInquiry() {
  if (isSubmitting.value) return

  isSubmitting.value = true
  submitError.value = ''
  formSubmitted.value = false

  const contactName = form.contactName
  const payload = {
    contact_person: form.contactName,
    phone: form.phone,
    company_brand: form.company,
    project_type: form.projectType,
    expected_quantity: form.quantity,
    delivery_city: form.city,
    budget_range: form.budget,
    requirement_description: form.message,
  }

  try {
    const response = await fetch('/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        'form-name': 'inquiry',
        'bot-field': '',
        ...payload,
      }).toString(),
    })

    if (!response.ok) {
      throw new Error('提交失败，请稍后再试。')
    }

    submittedContact.value = contactName
    formSubmitted.value = true
    Object.keys(form).forEach((key) => {
      form[key] = ''
    })
  } catch (error) {
    submitError.value = error instanceof Error ? error.message : '提交失败，请稍后再试。'
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  window.addEventListener('popstate', syncPath)
})

onBeforeUnmount(() => {
  window.removeEventListener('popstate', syncPath)
})

const page = computed(() => {
  if (currentPath.value === '/products') return 'products'
  if (currentPath.value === '/custom') return 'custom'
  if (currentPath.value === '/factory') return 'factory'
  if (currentPath.value === '/contact') return 'contact'
  return 'home'
})
</script>

<template>
  <div class="site-shell" :style="{ '--hero-image': `url(${heroImage})` }">
    <header class="topbar">
      <a class="brand" href="/" @click="goTo('/', $event)" aria-label="回到首页">
        <img class="brand-logo" :src="logoImage" alt="朗境家居 源头家居" />
      </a>

      <nav class="nav-links" aria-label="主导航">
        <a
          v-for="route in routes"
          :key="route.path"
          :href="route.path"
          :class="{ active: currentPath === route.path }"
          @click="goTo(route.path, $event)"
        >
          {{ route.label }}
        </a>
      </nav>
    </header>

    <main>
      <section v-if="page === 'home'" class="hero page-section">
        <div class="hero-copy">
          <p class="eyebrow">高端家居源头工厂 · 设计研发 · 柔性智造</p>
          <h1>让源头制造成为高端空间的确定性</h1>
          <p class="lead">
            朗境家居面向品牌商、设计机构、工程项目与全屋定制门店，提供轻奢家具研发、打样、生产、质检和交付服务。
          </p>
          <div class="hero-actions">
            <a href="/products" class="primary-link" @click="goTo('/products', $event)">查看产品</a>
            <a href="/contact" class="ghost-link" @click="goTo('/contact', $event)">提交需求</a>
          </div>
        </div>
        <div class="hero-panel" aria-label="工厂优势">
          <span>OEM / ODM / PROJECT</span>
          <strong>从材料到整案交付</strong>
          <p>软体、板式、木作、柜体与包装协同生产，让空间质感、工期和成本都可被管理。</p>
        </div>
      </section>

      <section v-if="page === 'home'" class="intro-band">
        <article>
          <span>01</span>
          <h2>研发前置</h2>
          <p>设计师与工艺工程师共同评审结构、材料、成本和交付方式，减少后期返工。</p>
        </article>
        <article>
          <span>02</span>
          <h2>工厂直供</h2>
          <p>自有生产线承接批量与小批量柔性订单，交期、品控和价格更透明。</p>
        </article>
        <article>
          <span>03</span>
          <h2>轻奢质感</h2>
          <p>精选木、石、皮、金属与灯光细节，呈现克制、耐看的高端居住体验。</p>
        </article>
      </section>

      <section v-if="page === 'home'" class="statement-section page-section">
        <p class="section-kicker">Factory to Home</p>
        <h2>我们不只生产家具，更生产可复制的高级感</h2>
        <p>
          高端项目最怕“样板好看、批量失控”。朗境从产品比例、材料色差、工艺节点、包装编号到安装顺序建立统一标准，让门店、项目方和终端客户获得一致体验。
        </p>
      </section>

      <section v-if="page === 'home'" class="service-matrix page-section">
        <article>
          <h3>品牌贴牌</h3>
          <p>支持外观微调、材料替换、包装规范和长期复购货号管理。</p>
        </article>
        <article>
          <h3>设计师项目</h3>
          <p>配合深化节点、定制尺寸和特殊材质，帮助方案顺利落地。</p>
        </article>
        <article>
          <h3>工程配套</h3>
          <p>适配地产样板间、酒店、公寓、民宿和办公空间批量采购。</p>
        </article>
        <article>
          <h3>门店上样</h3>
          <p>提供系列化产品组合、色板体系与展厅陈列建议。</p>
        </article>
      </section>

      <section v-if="page === 'home'" class="split-section">
        <div>
          <p class="section-kicker">Why Langjing</p>
          <h2>用源头工厂的效率，承接高端项目的细节</h2>
        </div>
        <ul class="elegant-list">
          <li>产品、材料、包装和质检统一建档，方便复购和追溯。</li>
          <li>从单品试样到整案批量交付，减少多供应商沟通成本。</li>
          <li>按品牌定位配置标准款、工程款和形象款，控制预算层级。</li>
          <li>关键节点提供进度同步，让项目方更好管理交付预期。</li>
        </ul>
      </section>

      <section v-if="page === 'products'" class="page-hero compact">
        <p class="eyebrow">产品中心</p>
        <h1>成套轻奢家居产品线</h1>
        <p class="lead">围绕客厅、餐厅、卧室与全屋柜体做系列化开发，适配门店上样、工程批量和品牌贴牌。</p>
      </section>

      <section v-if="page === 'products'" class="product-grid page-section">
        <article v-for="item in productLines" :key="item.name" class="product-card">
          <div class="material-strip"></div>
          <span>{{ item.material }}</span>
          <h2>{{ item.name }}</h2>
          <strong>{{ item.scope }}</strong>
          <p>{{ item.text }}</p>
        </article>
      </section>

      <section v-if="page === 'products'" class="content-band page-section">
        <div>
          <p class="section-kicker">Product Strategy</p>
          <h2>按渠道定位规划产品，而不是只做单件家具</h2>
        </div>
        <div class="three-column">
          <article>
            <h3>标准款</h3>
            <p>稳定供货、适合门店陈列和常规订单，尺寸、材料和包装规范完整。</p>
          </article>
          <article>
            <h3>工程款</h3>
            <p>在保持视觉质感的前提下优化结构与材料成本，适配批量项目。</p>
          </article>
          <article>
            <h3>形象款</h3>
            <p>强化木皮、金属、皮革和岩板细节，用于展厅主视觉和高端项目。</p>
          </article>
        </div>
      </section>

      <section v-if="page === 'products'" class="material-section">
        <div class="page-section material-layout">
          <div>
            <p class="section-kicker">Material Library</p>
            <h2>真实材料建立真实高级感</h2>
            <p>每个产品系列都配套色板、面料、五金和表面工艺记录，让长期供货保持稳定。</p>
          </div>
          <ul class="elegant-list">
            <li v-for="material in materialLibrary" :key="material">{{ material }}</li>
          </ul>
        </div>
      </section>

      <section v-if="page === 'products'" class="feature-row page-section">
        <div>
          <h2>统一色板，统一结构，统一包装</h2>
          <p>从选材到出厂建立标准，帮助客户降低复购、补货和跨城市交付的沟通成本。</p>
        </div>
        <ul>
          <li>支持来样复刻、系列开发、品牌贴牌和包装定制。</li>
          <li>支持小批量试单，确认市场反馈后再进入稳定供货。</li>
          <li>支持按户型、项目或门店陈列方案打包出货。</li>
        </ul>
      </section>

      <section v-if="page === 'custom'" class="page-hero compact warm">
        <p class="eyebrow">定制服务</p>
        <h1>从图纸到量产的一站式定制</h1>
        <p class="lead">支持设计公司、渠道门店和品牌客户进行尺寸、材质、结构、颜色与包装方式的深度定制。</p>
      </section>

      <section v-if="page === 'custom'" class="timeline page-section">
        <article v-for="(step, index) in customSteps" :key="step.title">
          <span>{{ String(index + 1).padStart(2, '0') }}</span>
          <h2>{{ step.title }}</h2>
          <p>{{ step.text }}</p>
        </article>
      </section>

      <section v-if="page === 'custom'" class="content-band page-section">
        <div>
          <p class="section-kicker">Customization Scope</p>
          <h2>定制不止改尺寸，也包括材料、结构和交付逻辑</h2>
        </div>
        <div class="two-column">
          <article>
            <h3>可定制内容</h3>
            <p>尺寸比例、木皮颜色、面料皮革、金属颜色、岩板纹理、拉手五金、灯光位置、包装唛头。</p>
          </article>
          <article>
            <h3>交付文件</h3>
            <p>产品清单、材料清单、报价表、生产排期、质检记录、包装编号和安装提示。</p>
          </article>
        </div>
      </section>

      <section v-if="page === 'custom'" class="precision-section page-section">
        <article>
          <span>Design</span>
          <h3>设计还原</h3>
          <p>把效果图里的比例、材质和氛围转译成可生产结构。</p>
        </article>
        <article>
          <span>Cost</span>
          <h3>成本控制</h3>
          <p>按预算区间配置标准材质、替代材质和工艺层级。</p>
        </article>
        <article>
          <span>Delivery</span>
          <h3>交付管理</h3>
          <p>按项目节点拆分打样、生产、包装和发运计划。</p>
        </article>
      </section>

      <section v-if="page === 'custom'" class="split-section dark">
        <div>
          <p class="section-kicker">Managed Customization</p>
          <h2>让每一次非标都可被管理</h2>
        </div>
        <p>
          定制不是临时改图，而是一套从需求记录到生产执行的闭环。朗境用编码、样板、质检表和包装规范控制细节，让轻奢质感在批量交付中保持一致。
        </p>
      </section>

      <section v-if="page === 'factory'" class="page-hero compact factory">
        <p class="eyebrow">源头工厂</p>
        <h1>看得见的产能，摸得到的品质</h1>
        <p class="lead">自有板式、软体、木作、涂装、装配与包装工段，支持来图加工、联合开发与品牌贴牌。</p>
      </section>

      <section v-if="page === 'factory'" class="stats-grid page-section">
        <article v-for="stat in factoryStats" :key="stat.label">
          <strong>{{ stat.value }}</strong>
          <span>{{ stat.label }}</span>
        </article>
      </section>

      <section v-if="page === 'factory'" class="factory-layout page-section">
        <div class="image-block"></div>
        <div>
          <p class="section-kicker">Quality System</p>
          <h2>从材料入库到成品出厂，全程可追溯</h2>
          <p>
            板材、面料、五金和石材按批次留样；关键工序设置首件确认、巡检和终检。每一件成品在包装前完成外观、结构、尺寸、五金和清洁检查。
          </p>
        </div>
      </section>

      <section v-if="page === 'factory'" class="factory-sections page-section">
        <article v-for="item in factorySections" :key="item.title">
          <h3>{{ item.title }}</h3>
          <p>{{ item.text }}</p>
        </article>
      </section>

      <section v-if="page === 'factory'" class="content-band page-section">
        <div>
          <p class="section-kicker">Traceable Production</p>
          <h2>品质管理落在每一道工序里</h2>
        </div>
        <ul class="elegant-list">
          <li>材料入库按批次留样，关键面料、木皮、五金建立项目档案。</li>
          <li>首件确认后进入批量生产，生产过程执行巡检和异常记录。</li>
          <li>成品包装前进行外观、结构、尺寸、五金和清洁检查。</li>
          <li>包装按客户、项目、楼栋、户型或安装顺序进行编号。</li>
        </ul>
      </section>

      <section v-if="page === 'contact'" class="page-hero compact contact">
        <p class="eyebrow">联系合作</p>
        <h1>把项目需求发给源头工厂</h1>
        <p class="lead">欢迎品牌商、设计机构、经销商与工程客户沟通打样、报价、排产和长期供货合作。</p>
      </section>

      <section v-if="page === 'contact'" class="contact-grid page-section">
        <article>
          <span>商务咨询</span>
          <h2>400-800-1688</h2>
          <p>周一至周六 09:00 - 18:00</p>
        </article>
        <article>
          <span>邮箱</span>
          <h2>partner@langjing-home.cn</h2>
          <p>建议附上空间图、产品清单或参考图片，便于快速评估。</p>
        </article>
        <article>
          <span>工厂地址</span>
          <h2>广东省佛山市顺德区龙江家具产业带</h2>
          <p>支持预约看样、验厂、选材与项目评审。</p>
        </article>
      </section>

      <section v-if="page === 'contact'" class="inquiry-section page-section">
        <div class="inquiry-copy">
          <p class="section-kicker">Inquiry Form</p>
          <h2>提交需求后，我们将按项目类型给出初步沟通建议</h2>
          <p>
            请尽量填写产品品类、数量、交付城市和预算范围。信息越完整，越能快速判断打样周期、报价区间和生产排期。
          </p>
          <div class="contact-notes">
            <span>常规需求 24 小时内响应</span>
            <span>批量项目可预约验厂</span>
            <span>支持 OEM / ODM / 工程配套</span>
          </div>
        </div>

        <form class="inquiry-form" @submit.prevent="submitInquiry">
          <label>
            联系人
            <input v-model.trim="form.contactName" required name="contactName" placeholder="请输入联系人姓名" />
          </label>
          <label>
            联系电话
            <input v-model.trim="form.phone" required name="phone" type="tel" placeholder="请输入手机号或座机" />
          </label>
          <label>
            公司/品牌
            <input v-model.trim="form.company" required name="company" placeholder="请输入公司或品牌名称" />
          </label>
          <label>
            项目类型
            <select v-model="form.projectType" required name="projectType">
              <option value="" disabled>请选择项目类型</option>
              <option v-for="item in projectTypes" :key="item" :value="item">{{ item }}</option>
            </select>
          </label>
          <label>
            项目数量
            <select v-model="form.quantity" required name="quantity">
              <option value="" disabled>请选择项目数量</option>
              <option v-for="item in quantityOptions" :key="item" :value="item">{{ item }}</option>
            </select>
          </label>
          <label>
            交付城市
            <input v-model.trim="form.city" required name="city" placeholder="例如：上海 / 成都 / 深圳" />
          </label>
          <label>
            预算区间
            <select v-model="form.budget" required name="budget">
              <option value="" disabled>请选择预算区间</option>
              <option v-for="item in budgetOptions" :key="item" :value="item">{{ item }}</option>
            </select>
          </label>
          <label class="full">
            需求说明
            <textarea
              v-model.trim="form.message"
              required
              name="message"
              rows="6"
              placeholder="请描述产品品类、风格参考、材质要求、交付时间或其他重点需求"
            ></textarea>
          </label>
          <button type="submit" :disabled="isSubmitting">
            {{ isSubmitting ? '提交中...' : '提交需求' }}
          </button>
          <p v-if="submitError" class="form-error">{{ submitError }}</p>
          <p v-if="formSubmitted" class="form-success">
            {{ submittedContact }}，需求已提交。我们会根据项目信息安排商务人员跟进。
          </p>
        </form>
      </section>
    </main>

    <footer class="site-footer">
      <strong>朗境家居源头工厂</strong>
      <span>高端轻奢家具 · 全屋定制 · OEM / ODM 生产合作</span>
    </footer>
  </div>
</template>
