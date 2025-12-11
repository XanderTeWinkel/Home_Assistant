import { ref, onMounted, onUnmounted } from "vue";
import axios from "axios";

const backendUrl = import.meta.env.VITE_BACKEND_URL;

export function useNews() {
  const news = ref([]);
  const currentIndex = ref(0);
  const error = ref<string | null>(null);
  const isHovering = ref(false);
  let interval: number | null = null;

  const fetchNews = async () => {
    try {
      const res = await axios.get(`${backendUrl}/nos-news`);
      news.value = res.data;
      currentIndex.value = 0;
      restart();
    } catch {
      error.value = "Failed to fetch news.";
    }
  };

  const start = () => {
    if (interval) return;
    interval = window.setInterval(() => {
      if (!isHovering.value) {
        currentIndex.value = (currentIndex.value + 1) % news.value.length;
      }
    }, 15000);
  };

  const stop = () => {
    if (interval) clearInterval(interval);
    interval = null;
  };

  const restart = () => {
    stop();
    start();
  };

  const goTo = (i: number) => {
    currentIndex.value = i;
    restart();
  };

  onMounted(() => {
    fetchNews();
    setInterval(fetchNews, 60 * 60 * 1000);
  });

  onUnmounted(stop);

  return { news, currentIndex, isHovering, goTo, error };
}
