// Ana JavaScript Dosyası

// Sayfa yüklendiğinde çalışacak kodlar
document.addEventListener('DOMContentLoaded', function() {
    
    // Bootstrap bileşenlerini başlat
    initBootstrapComponents();
    
    // Animasyonları başlat
    initAnimations();
    
    // Mesaj uyarılarını otomatik kapat
    initAlertDismissal();
    
    // Yorum yıldızlarını interaktif yap
    initRatingStars();
});

// Bootstrap bileşenlerini başlat
function initBootstrapComponents() {
    // Dropdown menüler
    const dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-toggle'));
    dropdownElementList.map(function (dropdownToggleEl) {
        return new bootstrap.Dropdown(dropdownToggleEl);
    });
    
    // Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Animasyonları başlat
function initAnimations() {
    // Sayfa içeriğine fade-in efekti ekle
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.classList.add('fade-in');
    }
    
    // Kitap kartlarına hover efekti ekle
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 10px 20px rgba(0, 0, 0, 0.1)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 5px rgba(0, 0, 0, 0.1)';
        });
    });
}

// Mesaj uyarılarını otomatik kapat
function initAlertDismissal() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        // 5 saniye sonra uyarıyı kapat
        setTimeout(() => {
            const closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        }, 5000);
    });
}

// Yorum yıldızlarını interaktif yap
function initRatingStars() {
    const ratingInputs = document.querySelectorAll('input[name="puan"]');
    const ratingLabels = document.querySelectorAll('.form-check-label[for^="puan"]');
    
    if (ratingInputs.length > 0) {
        // Yıldızların üzerine gelindiğinde
        ratingLabels.forEach((label, index) => {
            label.addEventListener('mouseenter', () => {
                // Mevcut ve önceki yıldızları vurgula
                for (let i = 0; i <= index; i++) {
                    ratingLabels[i].style.color = '#ffc107';
                    ratingLabels[i].style.fontWeight = 'bold';
                }
                
                // Sonraki yıldızları normal göster
                for (let i = index + 1; i < ratingLabels.length; i++) {
                    ratingLabels[i].style.color = '';
                    ratingLabels[i].style.fontWeight = '';
                }
            });
        });
        
        // Yıldızların üzerinden çıkıldığında
        const ratingContainer = ratingInputs[0].closest('.rating');
        if (ratingContainer) {
            ratingContainer.addEventListener('mouseleave', () => {
                // Seçili olmayan tüm yıldızları normal göster
                ratingLabels.forEach(label => {
                    label.style.color = '';
                    label.style.fontWeight = '';
                });
                
                // Seçili olan yıldızı vurgula
                ratingInputs.forEach((input, index) => {
                    if (input.checked) {
                        for (let i = 0; i <= index; i++) {
                            ratingLabels[i].style.color = '#ffc107';
                            ratingLabels[i].style.fontWeight = 'bold';
                        }
                    }
                });
            });
        }
        
        // Yıldıza tıklandığında
        ratingInputs.forEach((input, index) => {
            input.addEventListener('change', () => {
                // Tüm yıldızları normal göster
                ratingLabels.forEach(label => {
                    label.style.color = '';
                    label.style.fontWeight = '';
                });
                
                // Seçili yıldıza kadar vurgula
                for (let i = 0; i <= index; i++) {
                    ratingLabels[i].style.color = '#ffc107';
                    ratingLabels[i].style.fontWeight = 'bold';
                }
            });
        });
    }
} 