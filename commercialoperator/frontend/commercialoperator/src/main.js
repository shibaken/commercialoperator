import 'vite/modulepreload-polyfill';
// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

//import $ from 'jquery';
import moment from 'moment';
import swal from 'sweetalert2';
import jsZip from 'jszip';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import select2 from 'select2';
import _ from 'lodash';

window.$ = $;
window.jQuery = $;
window.moment = moment;
window.swal = swal;
window.JSZip = jsZip;
window.select2 = select2();
window._ = _;

import { createApp, configureCompat } from 'vue';
import router from './router';
import App from './App.vue';
import VueSelect from 'vue-select';
const app = createApp({
    router,
    ...App,
});

import helpers from '@/utils/helpers';
import { extendMoment } from 'moment-range';

import 'datatables.net-bs5';
import 'datatables.net-buttons-bs5';
import 'datatables.net-responsive-bs5';
import 'datatables.net-buttons/js/dataTables.buttons.js';
import 'datatables.net-buttons/js/buttons.html5.js';

import 'jquery-validation';

import 'sweetalert2/dist/sweetalert2.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import 'select2/dist/css/select2.min.css';
import 'select2-bootstrap-5-theme/dist/select2-bootstrap-5-theme.min.css';
import '@/../node_modules/datatables.net-bs5/css/dataTables.bootstrap5.min.css';
import '@/../node_modules/datatables.net-responsive-bs5/css/responsive.bootstrap5.min.css';


extendMoment(moment);
window.helpers = helpers;

const originalFetch = window.fetch.bind(window);

window.fetch = ((orig) => {
    return async (...args) => {
        // Normalize URL (string | URL | Request)
        let url;
        if (args[0] instanceof Request) {
            url = new URL(args[0].url, window.location.origin);
        } else if (args[0] instanceof URL) {
            url = new URL(args[0].href, window.location.origin);
        } else {
            url = new URL(String(args[0]), window.location.origin);
        }
        const sameOrigin = url.origin === window.location.origin;
        const isApi = sameOrigin && url.pathname.startsWith('/api');

        // Merge headers
        let headers = new Headers();
        if (args.length > 1 && args[1]?.headers) {
            headers =
                args[1].headers instanceof Headers
                    ? new Headers(args[1].headers)
                    : new Headers(args[1].headers);
        } else if (args[0] instanceof Request && args[0].headers) {
            headers = new Headers(args[0].headers);
        }

        if (sameOrigin)
            headers.set('X-CSRFToken', helpers.getCookie('csrftoken'));
        if (
            sameOrigin &&
            args.length > 1 &&
            typeof args[1]?.body === 'string'
        ) {
            headers.set('Content-Type', 'application/json');
        }

        if (args.length > 1) {
            args[1].headers = headers;
        } else {
            args.push({ headers });
        }

        const response = await orig(...args);

        if (response.status === 401 && isApi) {
            window.location.href =
                '/login/?next=' +
                encodeURIComponent(
                    window.location.pathname +
                        window.location.search +
                        window.location.hash
                );
            return response;
        } else if (response.status === 403) {
            swal.fire({
                icon: 'error',
                title: 'Access Denied',
                text: 'You do not have permission to perform this action.',
                customClass: { confirmButton: 'btn btn-primary' },
            });
        }
        return response;
    };
})(originalFetch);

configureCompat({
    WATCH_ARRAY: false, // Disable watch array for Vue 2 compatibility. I checked all watched objects/arrays to have the deep=true property set.
    RENDER_FUNCTION: false,
    COMPONENT_V_MODEL: false, // The only component in cols this affects is treeview.vue. There are other components that have a value prop, but they are not used with a v-model.
    ATTR_FALSE_VALUE: false,
});

// eslint-disable-next-line vue/component-definition-name-casing
app.component('v-select', VueSelect).use(router);
router.isReady().then(() => app.mount('#app'));

queueMicrotask(() => {
  const btn = document.getElementById('navbarScrollingDropdown');
  if (btn) {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      bootstrap.Dropdown.getOrCreateInstance(btn).toggle();
    });
  }
});
