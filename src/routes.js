import Directories from './components/Directories.vue';
import Settings from './components/Settings.vue';
import Home from './components/Home.vue';

export const routes = [
    { path: '/', component: Home },
    { path: '/directories', component: Directories },
    { path: '/settings', component: Settings }
]