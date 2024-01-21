import adapter from '@sveltejs/adapter-static';

export default {
  kit: {
    // Other configurations...

    adapter: adapter({
      // options are optional
      pages: 'build',
      assets: 'build',
      fallback: null
    })
  }
};