document.getElementById('downloadForm').addEventListener('submit', (e) => {
  e.preventDefault();
  const input = document.getElementById('url');
  const val = input.value.trim();
  const info = document.getElementById('info');
  info.textContent = '';

  if (!val) {
    info.textContent = '请输入有效的 URL。';
    return;
  }

  try {
    const u = new URL(val);
    // For a direct download, navigate to the proxy endpoint so browser handles save
    const proxyUrl = `/download?url=${encodeURIComponent(u.href)}`;
    window.location.href = proxyUrl;
  } catch (err) {
    info.textContent = 'URL 格式错误。';
  }
});

document.getElementById('clearBtn').addEventListener('click', () => {
  document.getElementById('url').value = '';
  document.getElementById('info').textContent = '';
});
