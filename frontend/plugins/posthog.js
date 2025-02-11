//./plugins/posthog.js
import posthog from "posthog-js";

export default {
  install(app) {
    app.config.globalProperties.$posthog = posthog.init(
      'phc_x8uieqh3y5q6dgnDEd20inToi0IkijdFRPCY64Po5Rn',
      {
        api_host: 'https://us.i.posthog.com',
      }
    );
  },
};