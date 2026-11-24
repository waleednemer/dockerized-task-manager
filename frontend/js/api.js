const API_URL = "/api";

async function request(path, options = {}) {
  const res = await fetch(API_URL + path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    if (body.error) throw new Error(body.error);
    throw new Error(
      res.status >= 500
        ? "الخدمة غير متاحة حاليًا. حاول بعد قليل."
        : "حدث خطأ غير متوقع"
    );
  }
  return res.status === 204 ? null : res.json();
}

const api = {
  list: () => request("/tasks"),
  create: (task) => request("/tasks", { method: "POST", body: JSON.stringify(task) }),
  update: (id, changes) => request(`/tasks/${id}`, { method: "PUT", body: JSON.stringify(changes) }),
  remove: (id) => request(`/tasks/${id}`, { method: "DELETE" }),
};
