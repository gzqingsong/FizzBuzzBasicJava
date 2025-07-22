// 全局变量
let svg, simulation, nodes, links;
let currentData = null;
let width, height;

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeVisualization();
    loadDefaultData();
    setupEventListeners();
});

// 初始化可视化
function initializeVisualization() {
    const container = d3.select('#visualization');
    const rect = container.node().getBoundingClientRect();
    width = rect.width;
    height = rect.height;

    // 创建SVG
    svg = container.append('svg')
        .attr('width', width)
        .attr('height', height);

    // 添加定义区域（用于箭头等）
    const defs = svg.append('defs');
    
    // 定义箭头标记
    defs.append('marker')
        .attr('id', 'arrowhead')
        .attr('viewBox', '-0 -5 10 10')
        .attr('refX', 15)
        .attr('refY', 0)
        .attr('orient', 'auto')
        .attr('markerWidth', 8)
        .attr('markerHeight', 8)
        .attr('xoverflow', 'visible')
        .append('svg:path')
        .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
        .attr('fill', 'rgba(255, 255, 255, 0.6)')
        .style('stroke', 'none');

    // 创建力导向图模拟
    simulation = d3.forceSimulation()
        .force('link', d3.forceLink().id(d => d.id).distance(80))
        .force('charge', d3.forceManyBody().strength(-300))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collision', d3.forceCollide().radius(d => Math.sqrt(d.size) * 2));
}

// 加载默认数据
async function loadDefaultData() {
    try {
        showLoading();
        const response = await fetch('/api/data');
        const data = await response.json();
        updateVisualization(data);
    } catch (error) {
        console.error('加载数据失败:', error);
        showError('加载数据失败，请刷新页面重试');
    }
}

// 显示加载状态
function showLoading() {
    const container = d3.select('#visualization');
    container.html('<div class="loading"><div class="spinner"></div>正在加载数据...</div>');
}

// 显示错误信息
function showError(message) {
    const container = d3.select('#visualization');
    container.html(`<div class="loading" style="color: #ff6b6b;"><i class="fas fa-exclamation-triangle"></i> ${message}</div>`);
}

// 更新可视化
function updateVisualization(data) {
    currentData = data;
    
    // 重新初始化SVG
    d3.select('#visualization').selectAll('*').remove();
    initializeVisualization();
    
    nodes = [...data.nodes];
    links = [...data.links];

    // 更新统计信息
    updateStats();

    // 创建连接线
    const linkGroup = svg.append('g').attr('class', 'links');
    const linkElements = linkGroup.selectAll('line')
        .data(links)
        .enter()
        .append('line')
        .attr('class', 'link')
        .attr('marker-end', 'url(#arrowhead)');

    // 创建节点
    const nodeGroup = svg.append('g').attr('class', 'nodes');
    const nodeElements = nodeGroup.selectAll('circle')
        .data(nodes)
        .enter()
        .append('circle')
        .attr('class', 'node')
        .attr('r', d => Math.sqrt(d.size) * 1.5)
        .attr('fill', d => d.color)
        .call(drag(simulation))
        .on('mouseover', handleNodeMouseOver)
        .on('mouseout', handleNodeMouseOut)
        .on('click', handleNodeClick);

    // 创建标签
    const labelGroup = svg.append('g').attr('class', 'labels');
    const labelElements = labelGroup.selectAll('text')
        .data(nodes)
        .enter()
        .append('text')
        .attr('class', d => `node-label ${d.size > 30 ? 'large' : ''}`)
        .text(d => d.id.length > 15 ? d.id.substring(0, 12) + '...' : d.id);

    // 启动模拟
    simulation.nodes(nodes).on('tick', () => {
        linkElements
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);

        nodeElements
            .attr('cx', d => d.x)
            .attr('cy', d => d.y);

        labelElements
            .attr('x', d => d.x)
            .attr('y', d => d.y + 5);
    });

    simulation.force('link').links(links);
    simulation.alpha(1).restart();
}

// 节点拖拽
function drag(simulation) {
    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }

    function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

    return d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended);
}

// 节点鼠标悬停
function handleNodeMouseOver(event, d) {
    // 高亮当前节点和相关连接
    highlightNode(d);
    
    // 显示工具提示
    showTooltip(event, d);
}

// 节点鼠标离开
function handleNodeMouseOut(event, d) {
    // 移除高亮
    clearHighlight();
    
    // 隐藏工具提示
    hideTooltip();
}

// 节点点击
function handleNodeClick(event, d) {
    console.log('点击节点:', d);
    // 可以在这里添加更多交互功能
}

// 高亮节点和相关连接
function highlightNode(node) {
    // 获取相关连接
    const connectedLinks = links.filter(l => l.source.id === node.id || l.target.id === node.id);
    const connectedNodes = new Set();
    connectedLinks.forEach(l => {
        connectedNodes.add(l.source.id);
        connectedNodes.add(l.target.id);
    });

    // 高亮节点
    svg.selectAll('.node')
        .classed('highlighted', d => connectedNodes.has(d.id));

    // 高亮连接
    svg.selectAll('.link')
        .classed('highlighted', d => d.source.id === node.id || d.target.id === node.id);
}

// 清除高亮
function clearHighlight() {
    svg.selectAll('.node').classed('highlighted', false);
    svg.selectAll('.link').classed('highlighted', false);
}

// 显示工具提示
function showTooltip(event, d) {
    const tooltip = d3.select('#tooltip');
    const connectedCount = links.filter(l => l.source.id === d.id || l.target.id === d.id).length;
    
    tooltip.html(`
        <h6>${d.id}</h6>
        <p><strong>分组:</strong> ${d.group}</p>
        <p><strong>大小:</strong> ${d.size}</p>
        <p><strong>连接数:</strong> ${connectedCount}</p>
    `)
    .style('left', (event.pageX + 10) + 'px')
    .style('top', (event.pageY - 10) + 'px')
    .classed('show', true);
}

// 隐藏工具提示
function hideTooltip() {
    d3.select('#tooltip').classed('show', false);
}

// 更新统计信息
function updateStats() {
    const nodeCount = document.getElementById('nodeCount');
    const linkCount = document.getElementById('linkCount');
    
    // 添加动画效果
    nodeCount.classList.add('stats-number');
    linkCount.classList.add('stats-number');
    
    nodeCount.textContent = nodes.length;
    linkCount.textContent = links.length;
    
    // 触发更新动画
    setTimeout(() => {
        nodeCount.classList.add('updated');
        linkCount.classList.add('updated');
        setTimeout(() => {
            nodeCount.classList.remove('updated');
            linkCount.classList.remove('updated');
        }, 500);
    }, 100);
}

// 设置事件监听器
function setupEventListeners() {
    // 搜索功能
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', handleSearch);

    // 显示设置
    const showLabels = document.getElementById('showLabels');
    const showLinks = document.getElementById('showLinks');
    
    showLabels.addEventListener('change', toggleLabels);
    showLinks.addEventListener('change', toggleLinks);

    // 力度调节
    const forceStrength = document.getElementById('forceStrength');
    forceStrength.addEventListener('input', adjustForceStrength);

    // 窗口大小调整
    window.addEventListener('resize', handleResize);
}

// 搜索处理
function handleSearch(event) {
    const searchTerm = event.target.value.toLowerCase();
    
    svg.selectAll('.node')
        .classed('search-highlight', d => {
            return searchTerm && d.id.toLowerCase().includes(searchTerm);
        });
}

// 切换标签显示
function toggleLabels() {
    const showLabels = document.getElementById('showLabels').checked;
    svg.selectAll('.node-label').style('display', showLabels ? 'block' : 'none');
}

// 切换连接线显示
function toggleLinks() {
    const showLinks = document.getElementById('showLinks').checked;
    svg.selectAll('.link').style('display', showLinks ? 'block' : 'none');
}

// 调整力度
function adjustForceStrength() {
    const strength = parseFloat(document.getElementById('forceStrength').value);
    simulation.force('charge').strength(-300 * strength);
    simulation.alpha(0.3).restart();
}

// 重置可视化
function resetVisualization() {
    if (currentData) {
        updateVisualization(currentData);
    }
}

// 处理窗口大小调整
function handleResize() {
    const container = d3.select('#visualization');
    const rect = container.node().getBoundingClientRect();
    width = rect.width;
    height = rect.height;

    svg.attr('width', width).attr('height', height);
    simulation.force('center', d3.forceCenter(width / 2, height / 2));
    simulation.alpha(0.3).restart();
}

// 文件上传功能
async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        showUploadStatus('请选择一个文件', 'danger');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        showUploadStatus('正在上传文件...', 'info');
        
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            showUploadStatus('文件上传成功！正在更新可视化...', 'success');
            updateVisualization(result);
            
            // 关闭模态框
            setTimeout(() => {
                const modal = bootstrap.Modal.getInstance(document.getElementById('uploadModal'));
                modal.hide();
                clearUploadStatus();
            }, 1500);
        } else {
            showUploadStatus(result.error || '上传失败', 'danger');
        }
    } catch (error) {
        console.error('上传错误:', error);
        showUploadStatus('网络错误，请重试', 'danger');
    }
}

// 显示上传状态
function showUploadStatus(message, type) {
    const statusDiv = document.getElementById('uploadStatus');
    statusDiv.innerHTML = `<div class="alert alert-${type}" role="alert">${message}</div>`;
}

// 清除上传状态
function clearUploadStatus() {
    document.getElementById('uploadStatus').innerHTML = '';
    document.getElementById('fileInput').value = '';
}