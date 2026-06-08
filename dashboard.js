/* LÓGICA DEL DASHBOARD - COMPONENTE REUTILIZABLE */

// Cargar el dashboard en la página
async function cargarDashboard() {
    try {
        const res = await fetch('/dashboard.html');
        const html = await res.text();
        
        // Insertar dashboard antes del body
        document.body.insertAdjacentHTML('afterbegin', html);
        
        // Cargar estilos
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '/dashboard.css';
        document.head.appendChild(link);
        
        // Inicializar funciones
        inicializarDashboard();
    } catch (err) {
        console.error('Error cargando dashboard:', err);
    }
}

// Inicializar dashboard
async function inicializarDashboard() {
    cargarSesion();
    actualizarNavBar();
    actualizarHora();
    setInterval(actualizarHora, 1000);
    setInterval(cargarNotificaciones, 5000);
}

// Cargar sesión del usuario
async function cargarSesion() {
    try {
        const res = await fetch('/api/sesion');
        if (res.ok) {
            const sesion = await res.json();
            if (sesion.logueado) {
                const elem1 = document.getElementById('perfil-nombre-dashboard');
                const elem2 = document.getElementById('perfil-rol-dashboard');
                const elem3 = document.getElementById('perfil-email-dashboard');
                if (elem1) elem1.textContent = sesion.usuario_nombre;
                if (elem2) elem2.textContent = sesion.usuario_rol;
                if (elem3) elem3.textContent = sesion.usuario_email;
            }
        }
    } catch (err) {
        console.error('Error cargando sesión:', err);
    }
}

// Actualizar navbar según página actual
function actualizarNavBar() {
    const pagina = obtenerPaginaActual();
    const navItems = document.querySelectorAll('.nav-item[data-page]');
    
    navItems.forEach(item => {
        item.classList.remove('active');
        if (item.dataset.page === pagina) {
            item.classList.add('active');
        }
    });
}

// Obtener página actual
function obtenerPaginaActual() {
    const url = window.location.pathname;
    if (url.includes('/panel')) return 'panel';
    if (url.includes('/usuarios')) return 'usuarios';
    if (url.includes('/auditoria')) return 'auditoria';
    if (url.includes('/estadosys')) return 'estadosys';
    return null;
}

// Actualizar hora en perfil
function actualizarHora() {
    const ahora = new Date();
    const hora = ahora.toLocaleTimeString('es-ES', { 
        hour: '2-digit', 
        minute: '2-digit', 
        second: '2-digit'
    });
    const elem = document.getElementById('perfil-hora-dashboard');
    if (elem) elem.textContent = hora;
}

// Abrir modal de perfil
function abrirPerfil() {
    const modal = document.getElementById('modalPerfil');
    if (modal) {
        modal.classList.add('show');
        actualizarHora();
    }
}

// Cerrar modal de perfil
function cerrarPerfil() {
    const modal = document.getElementById('modalPerfil');
    if (modal) modal.classList.remove('show');
}

// Cerrar sesión
function cerrarSesion() {
    if (confirm('¿Deseas cerrar sesión?')) {
        window.location.href = '/logout';
    }
}

// Cargar notificaciones en tiempo real
async function cargarNotificaciones() {
    try {
        const res = await fetch('/auditoria_datos');
        const logs = await res.json();
        
        const notificaciones = logs.slice(-5).reverse();
        
        const badge = document.getElementById('notif-badge');
        if (badge) badge.textContent = notificaciones.length;
        
        const lista = document.getElementById('notif-list-dashboard');
        if (!lista) return;
        
        lista.innerHTML = '';
        
        if (notificaciones.length === 0) {
            lista.innerHTML = '<p style="text-align:center;color:#999;padding:20px;">No hay notificaciones</p>';
            return;
        }
        
        notificaciones.forEach(log => {
            const icono = log.metodo?.includes('QR') ? 'bi-qr-code-scan' :
                         log.metodo?.includes('Huella') ? 'bi-fingerprint' :
                         log.metodo?.includes('Tarjeta') ? 'bi-credit-card-2-front-fill' : 'bi-info-circle';
            
            const estado = log.estado === 'activo' ? 'permitido' : 'denegado';
            const estadoText = log.estado === 'activo' ? 'PERMITIDO' : 'DENEGADO';
            
            const item = document.createElement('div');
            item.className = `notif-item-dashboard ${estado}`;
            item.innerHTML = `
                <i class="bi ${icono} notif-icon-dashboard"></i>
                <div class="notif-content-dashboard">
                    <strong>${log.nombre || 'Usuario ' + log.usuario_id}</strong>
                    <small>${log.metodo || 'Método desconocido'}</small>
                    <small>${log.ubicacion || 'Ubicación'}</small>
                    <small>${log.fecha || 'Hora no disponible'}</small>
                </div>
                <span class="notif-estado-dashboard ${estado}">${estadoText}</span>
            `;
            lista.appendChild(item);
        });
    } catch (err) {
        console.error('Error cargando notificaciones:', err);
    }
}

// Abrir modal de notificaciones
function abrirNotificaciones() {
    const modal = document.getElementById('modalNotificaciones');
    if (modal) {
        modal.classList.add('show');
        cargarNotificaciones();
    }
}

// Cerrar modal de notificaciones
function cerrarNotificaciones() {
    const modal = document.getElementById('modalNotificaciones');
    if (modal) modal.classList.remove('show');
}

// Cerrar modales al hacer click fuera
window.addEventListener('click', function(event) {
    const modalPerfil = document.getElementById('modalPerfil');
    const modalNotif = document.getElementById('modalNotificaciones');
    
    if (modalPerfil && event.target === modalPerfil) {
        modalPerfil.classList.remove('show');
    }
    if (modalNotif && event.target === modalNotif) {
        modalNotif.classList.remove('show');
    }
});

// Cargar dashboard cuando el DOM está listo
document.addEventListener('DOMContentLoaded', cargarDashboard);
