class FaceAuthHandler {
    constructor() {
        this.stream = null;
        this.isActive = false;
    }

    async startCamera(event, mode = 'login') {
        if (event) {
            event.preventDefault();
            event.stopPropagation();
        }

        // Nếu camera đang bật, tắt nó đi
        if (this.isActive) {
            this.stopCamera();
            return;
        }

        // Lấy các elements dựa theo mode
        const videoElement = mode === 'login' ? 
            document.getElementById('faceVideo') : 
            document.getElementById('faceVideoSignup');
        const avatarElement = mode === 'login' ? 
            document.getElementById('defaultAvatar') : 
            document.getElementById('signupDefaultAvatar');
        const previewElement = mode === 'login' ? 
            document.getElementById('cameraPreview') : 
            document.getElementById('signupCameraPreview');

        try {
            console.log('Starting camera...'); // Debug log
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: 180,
                    height: 180,
                    facingMode: 'user'
                }
            });

            if (videoElement && this.stream) {
                videoElement.srcObject = this.stream;
                avatarElement.style.display = 'none';
                previewElement.style.display = 'block';
                this.isActive = true;
                console.log('Camera started successfully'); // Debug log
            }
        } catch (error) {
            console.error('Error accessing camera:', error);
        }
    }

    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());

            // Reset all elements
            ['defaultAvatar', 'signupDefaultAvatar'].forEach(id => {
                const avatar = document.getElementById(id);
                if (avatar) avatar.style.display = 'block';
            });

            ['cameraPreview', 'signupCameraPreview'].forEach(id => {
                const preview = document.getElementById(id);
                if (preview) preview.style.display = 'none';
            });

            this.stream = null;
            this.isActive = false;
            console.log('Camera stopped'); // Debug log
        }
    }

    async authenticateWithFace(mode) {
        const videoElement = mode === 'login' ? 
            document.getElementById('faceVideo') : 
            document.getElementById('faceVideoSignup');

        if (!videoElement || !videoElement.srcObject) {
            console.error('No video stream available');
            return;
        }

        // Capture the current frame
        const canvas = document.createElement('canvas');
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        canvas.getContext('2d').drawImage(videoElement, 0, 0);
        const imageData = canvas.toDataURL('image/jpeg');

        try {
            // Tạm thời console.log để test
            console.log(`Face ${mode} attempted`);
            // Sau này sẽ gửi imageData lên server để xử lý
            
            // Dừng camera sau khi xử lý xong
            this.stopCamera();
        } catch (error) {
            console.error('Face authentication error:', error);
        }
    }
}

// Initialize Face Auth
const faceAuth = new FaceAuthHandler();

// Function to handle starting face auth
function startFaceAuth(event) {
    faceAuth.startCamera(event);
}

// Stop camera when navigating away
window.addEventListener('beforeunload', () => {
    faceAuth.stopCamera();
});