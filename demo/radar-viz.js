// CivicGuardian AI - Risk Radar Visualization
// Canvas-based radar chart for risk impact visualization

class RiskRadar {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) {
            console.error(`Canvas element with id "${canvasId}" not found`);
            return;
        }
        
        this.ctx = this.canvas.getContext('2d');
        this.centerX = this.canvas.width / 2;
        this.centerY = this.canvas.height / 2;
        this.maxRadius = Math.min(this.centerX, this.centerY) - 40;
        
        // Sky-Blue Fluent color palette
        this.colors = {
            skyBlue: '#005EB8',
            skyCyan: '#00A9CE',
            nhsGreen: '#007F3B',
            gridLine: 'rgba(0, 94, 184, 0.15)',
            labelText: '#64748B',
            axisLine: 'rgba(0, 94, 184, 0.3)'
        };
        
        // Default data
        this.data = {
            urgency: 0,
            complexity: 0,
            confidence: 0
        };
        
        this.labels = ['Urgency', 'Complexity', 'Confidence'];
        this.animationProgress = 0;
    }
    
    // Draw the radar grid
    drawGrid() {
        const ctx = this.ctx;
        const levels = 5;
        
        // Draw concentric circles
        for (let i = 1; i <= levels; i++) {
            const radius = (this.maxRadius / levels) * i;
            
            ctx.beginPath();
            ctx.arc(this.centerX, this.centerY, radius, 0, Math.PI * 2);
            ctx.strokeStyle = this.colors.gridLine;
            ctx.lineWidth = 1;
            ctx.stroke();
            
            // Draw level labels
            if (i === levels) {
                ctx.fillStyle = this.colors.labelText;
                ctx.font = '11px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('100%', this.centerX, this.centerY - radius - 8);
            }
        }
        
        // Draw axes
        const angleStep = (Math.PI * 2) / this.labels.length;
        
        for (let i = 0; i < this.labels.length; i++) {
            const angle = angleStep * i - Math.PI / 2;
            const x = this.centerX + Math.cos(angle) * this.maxRadius;
            const y = this.centerY + Math.sin(angle) * this.maxRadius;
            
            // Draw axis line
            ctx.beginPath();
            ctx.moveTo(this.centerX, this.centerY);
            ctx.lineTo(x, y);
            ctx.strokeStyle = this.colors.axisLine;
            ctx.lineWidth = 1.5;
            ctx.stroke();
            
            // Draw axis label
            const labelX = this.centerX + Math.cos(angle) * (this.maxRadius + 25);
            const labelY = this.centerY + Math.sin(angle) * (this.maxRadius + 25);
            
            ctx.fillStyle = this.colors.labelText;
            ctx.font = '600 13px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(this.labels[i], labelX, labelY);
        }
    }
    
    // Draw the data polygon
    drawData() {
        const ctx = this.ctx;
        const angleStep = (Math.PI * 2) / this.labels.length;
        const values = [
            this.data.urgency * this.animationProgress,
            this.data.complexity * this.animationProgress,
            this.data.confidence * this.animationProgress
        ];
        
        // Draw filled polygon
        ctx.beginPath();
        
        for (let i = 0; i < values.length; i++) {
            const angle = angleStep * i - Math.PI / 2;
            const radius = (values[i] / 100) * this.maxRadius;
            const x = this.centerX + Math.cos(angle) * radius;
            const y = this.centerY + Math.sin(angle) * radius;
            
            if (i === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        }
        
        ctx.closePath();
        
        // Fill with gradient
        const gradient = ctx.createRadialGradient(
            this.centerX, this.centerY, 0,
            this.centerX, this.centerY, this.maxRadius
        );
        gradient.addColorStop(0, 'rgba(0, 169, 206, 0.4)');
        gradient.addColorStop(1, 'rgba(0, 94, 184, 0.2)');
        
        ctx.fillStyle = gradient;
        ctx.fill();
        
        // Stroke outline
        ctx.strokeStyle = this.colors.skyCyan;
        ctx.lineWidth = 2.5;
        ctx.stroke();
        
        // Draw data points
        for (let i = 0; i < values.length; i++) {
            const angle = angleStep * i - Math.PI / 2;
            const radius = (values[i] / 100) * this.maxRadius;
            const x = this.centerX + Math.cos(angle) * radius;
            const y = this.centerY + Math.sin(angle) * radius;
            
            // Outer glow
            ctx.beginPath();
            ctx.arc(x, y, 8, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(0, 169, 206, 0.3)';
            ctx.fill();
            
            // Inner circle
            ctx.beginPath();
            ctx.arc(x, y, 5, 0, Math.PI * 2);
            ctx.fillStyle = this.colors.skyCyan;
            ctx.fill();
            ctx.strokeStyle = '#FFFFFF';
            ctx.lineWidth = 2;
            ctx.stroke();
        }
    }
    
    // Clear canvas
    clear() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }
    
    // Render the complete radar chart
    render() {
        this.clear();
        this.drawGrid();
        this.drawData();
    }
    
    // Update data with animation
    updateData(urgency, complexity, confidence) {
        this.data = {
            urgency: Math.min(100, Math.max(0, urgency)),
            complexity: Math.min(100, Math.max(0, complexity)),
            confidence: Math.min(100, Math.max(0, confidence))
        };
        
        // Animate from 0 to 1
        this.animationProgress = 0;
        const duration = 1000; // 1 second
        const startTime = Date.now();
        
        const animate = () => {
            const elapsed = Date.now() - startTime;
            this.animationProgress = Math.min(1, elapsed / duration);
            
            // Easing function (ease-out cubic)
            const eased = 1 - Math.pow(1 - this.animationProgress, 3);
            this.animationProgress = eased;
            
            this.render();
            
            if (elapsed < duration) {
                requestAnimationFrame(animate);
            }
        };
        
        animate();
    }
    
    // Initialize with default view
    init() {
        this.render();
    }
}

// Export for use in demo.js
window.RiskRadar = RiskRadar;
