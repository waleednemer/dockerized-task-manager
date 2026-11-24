const $ = (s) => document.querySelector(s);
const STATUS = { todo: "للتنفيذ", doing: "قيد العمل", done: "مكتملة" };
const PRIORITY = { low: "منخفضة", medium: "متوسطة", high: "عالية" };
let tasks = [];
let filter = "all";

function showError(msg) {
  const el = $("#error");
  el.textContent = msg;
  el.hidden = !msg;
}

async function run(action) {
  try {
    showError("");
    await action();
  } catch (e) {
    console.error(e);
    showError(e instanceof TypeError ? "تعذر الاتصال بالخادم. تأكد من تشغيل الـ backend." : e.message);
  }
  render();
}

function el(tag, cls, text) {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (text) n.textContent = text;
  return n;
}

function card(t) {
  const li = el("li", `task ${t.status} p-${t.priority}`);
  const info = el("div", "info");
  const meta = `الأولوية: ${PRIORITY[t.priority]}` + (t.due_date ? `، الموعد: ${t.due_date}` : "");
  info.append(el("span", "title", t.title), el("span", "meta", meta));

  const sel = el("select");
  sel.setAttribute("aria-label", "الحالة");
  for (const [v, label] of Object.entries(STATUS)) sel.add(new Option(label, v, false, v === t.status));
  sel.onchange = () => run(async () => {
    const updated = await api.update(t.id, { status: sel.value });
    tasks = tasks.map((x) => (x.id === t.id ? updated : x));
  });

  const del = el("button", "del", "حذف");
  del.onclick = () => run(async () => {
    await api.remove(t.id);
    tasks = tasks.filter((x) => x.id !== t.id);
  });

  li.append(info, sel, del);
  return li;
}

function render() {
  const items = tasks.filter((t) => filter === "all" || t.status === filter);
  $("#list").replaceChildren(...items.map(card));
  $("#empty").hidden = items.length > 0;
  $("#count").textContent = `${tasks.filter((t) => t.status !== "done").length} مهمة مفتوحة`;
}

$("#form").onsubmit = (e) => {
  e.preventDefault();
  run(async () => {
    const created = await api.create({
      title: $("#title").value,
      priority: $("#priority").value,
      due_date: $("#due").value,
    });
    tasks.unshift(created);
    $("#form").reset();
  });
};

$("#filters").onclick = (e) => {
  if (!e.target.dataset.f) return;
  filter = e.target.dataset.f;
  document.querySelectorAll("#filters button").forEach((b) => b.classList.toggle("on", b === e.target));
  render();
};

run(async () => { tasks = await api.list(); });
