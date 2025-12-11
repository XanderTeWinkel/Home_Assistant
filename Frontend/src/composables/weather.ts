import { ref, onMounted } from "vue";
import axios from "axios";

const backendUrl = import.meta.env.VITE_BACKEND_URL;

export function useWeather() {
  const weather = ref(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const fetchWeather = async () => {
    loading.value = true;
    try {
      const res = await axios.get(`${backendUrl}/weather`);
      weather.value = res.data;
    } catch {
      error.value = "Failed to fetch weather.";
    } finally {
      loading.value = false;
    }
  };

  onMounted(() => {
    fetchWeather();
    setInterval(fetchWeather, 10 * 60 * 1000);
  });

  return { weather, loading, error, fetchWeather };
}
