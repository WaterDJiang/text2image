document.addEventListener('DOMContentLoaded', function() {
    const uploadCard = document.getElementById('uploadCard');
    const previewImage = document.getElementById('previewImage');
    const uploadPlaceholder = document.getElementById('uploadPlaceholder');
    const generateBtn = document.getElementById('generateBtn');
    const resultSection = document.getElementById('resultSection');
    const generatedImage = document.getElementById('generatedImage');
    const generatedText = document.getElementById('generatedText');
    const copyBtn = document.getElementById('copyBtn');
    const shareBtn = document.getElementById('shareBtn');

    let selectedFile = null;

    // 处理拖拽上传
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadCard.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadCard.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadCard.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        uploadCard.classList.add('drag-hover');
    }

    function unhighlight(e) {
        uploadCard.classList.remove('drag-hover');
    }

    uploadCard.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    function validateFile(file) {
        // 检查文件大小
        if (file.size > 5 * 1024 * 1024) {
            showToast('图片大小不能超过 5MB');
            return false;
        }

        // 检查文件类型
        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
        if (!allowedTypes.includes(file.type)) {
            showToast('请上传 JPG、PNG、GIF 或 WEBP 格式的图片');
            return false;
        }

        return true;
    }

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            if (!validateFile(file)) {
                return;
            }
            
            selectedFile = file;
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImage.src = e.target.result;
                previewImage.style.display = 'block';
                uploadPlaceholder.style.display = 'none';
            };
            reader.readAsDataURL(selectedFile);
        }
    }

    // 点击上传
    uploadCard.addEventListener('click', function() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*';
        input.onchange = function(event) {
            handleFiles(event.target.files);
        };
        input.click();
    });

    generateBtn.addEventListener('click', debounce(async function() {
        if (!selectedFile) {
            showToast('请先上传图片');
            return;
        }

        // 显示加载状态
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<i class="material-icons loading">sync</i><span>生成中...</span>';
        
        const loadingAnimation = document.getElementById('loadingAnimation');
        const resultPreview = document.querySelector('.result-preview');
        
        loadingAnimation.style.display = 'flex';
        resultPreview.classList.remove('show');
        resultPreview.style.opacity = '0';

        const formData = new FormData();
        formData.append('image', selectedFile);
        formData.append('type', 'sarcastic');  // 这里改为 sarcastic

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            // 显示结果区域
            resultSection.style.display = 'block';

            // 处理错误情况
            if (!response.ok || data.error) {
                if (data.type === 'recharge') {
                    generatedText.innerHTML = `
                        <div class="error-message fun-error">
                            <div class="error-icon-large">
                                <i class="material-icons">battery_alert</i>
                            </div>
                            <div class="error-content">
                                <h3>啊哦...AI 能量不足啦！</h3>
                                <p>${data.error}</p>
                                <div class="error-tips">
                                    <p>您可以：</p>
                                    <ul>
                                        <li>稍等片刻，说不定主人正在充值</li>
                                        <li>过会儿再来，让我休息一下</li>
                                        <li>去喝杯咖啡，等我恢复精力</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    `;
                } else {
                    generatedText.innerHTML = `
                        <div class="error-message">
                            <i class="material-icons error-icon">error_outline</i>
                            <p>${data.error || '生成失败，请重试'}</p>
                        </div>
                    `;
                }
                generatedText.style.display = 'block';
                generatedImage.style.display = 'none';
                loadingAnimation.style.display = 'none';
                resultPreview.classList.add('show');
                resultPreview.style.opacity = '1';
                return;
            }

            // 处理成功情况
            if (data.output) {
                generatedImage.src = data.output;
                generatedImage.style.display = 'block';
                generatedText.style.display = 'none';
                
                generatedImage.onload = () => {
                    loadingAnimation.style.display = 'none';
                    resultPreview.classList.add('show');
                    resultPreview.style.opacity = '1';
                };
                
                generatedImage.onerror = () => {
                    generatedText.innerHTML = `
                        <div class="error-message">
                            <i class="material-icons error-icon">error_outline</i>
                            <p>图片加载失败</p>
                        </div>
                    `;
                    generatedText.style.display = 'block';
                    generatedImage.style.display = 'none';
                    loadingAnimation.style.display = 'none';
                };
            } else {
                generatedText.textContent = typeof data === 'string' ? data : JSON.stringify(data);
                generatedText.style.display = 'block';
                generatedImage.style.display = 'none';
                loadingAnimation.style.display = 'none';
                resultPreview.classList.add('show');
                resultPreview.style.opacity = '1';
            }

            resultSection.scrollIntoView({ behavior: 'smooth' });

        } catch (error) {
            console.error('Error:', error);
            resultSection.style.display = 'block';
            generatedText.innerHTML = `
                <div class="error-message">
                    <i class="material-icons error-icon">error_outline</i>
                    <p>网络错误，请稍后重试</p>
                </div>
            `;
            generatedText.style.display = 'block';
            generatedImage.style.display = 'none';
            loadingAnimation.style.display = 'none';
            resultPreview.classList.add('show');
            resultPreview.style.opacity = '1';
            showToast('生成失败');
        } finally {
            generateBtn.disabled = false;
            generateBtn.innerHTML = '<i class="material-icons">auto_awesome</i><span>生成毒舌文案</span>';
        }
    }, 500));

    // 修改查看图片按钮的处理逻辑
    copyBtn.addEventListener('click', function() {
        if (generatedImage.style.display !== 'none' && generatedImage.src) {
            // 在新窗口打开图片
            window.open(generatedImage.src, '_blank');
        } else {
            showToast('没有可查看的图片');
        }
    });

    // 分享功能
    shareBtn.addEventListener('click', async function() {
        if (navigator.share) {
            try {
                const shareData = {
                    title: 'AI生成的内容',
                    text: generatedText.style.display !== 'none' ? generatedText.textContent : '查看AI生成的图片',
                    url: generatedImage.style.display !== 'none' ? generatedImage.src : window.location.href
                };
                await navigator.share(shareData);
                showToast('分享成功');
            } catch (error) {
                if (error.name !== 'AbortError') {
                    showToast('分享失败');
                }
            }
        } else {
            showToast('您的浏览器不支持分享功能');
        }
    });

    function showToast(message) {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.classList.add('show');
        }, 100);

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(toast);
            }, 300);
        }, 3000);
    }

    // 添加更多的加载状态反馈
    loadingAnimation.innerHTML = `
        <div class="spinner"></div>
        <p>AI 正在思考中...</p>
        <p class="loading-tips">这可能需要几秒钟时间</p>
    `;
}); 