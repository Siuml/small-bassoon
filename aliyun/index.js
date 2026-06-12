// pages/aliyun/aliyun.js
const mqtt = require('../../utils/mqtt.min.js');
const aliyunConfig = require('../../config/aliyun');

Page({
  data: {
    sensorData: {
      temperature: null,    // 温度
      humidity: null,       // 湿度
      airQuality: null,     // 空气质量
      dust: null,           // 粉尘浓度
      status: true          // 设备状态
    },
    connectionStatus: "未连接"
  },

  onLoad() {
    this.connectAliyun();
  },

  onUnload() {
    if (this.client) {
      this.client.end();
      console.log('MQTT连接已断开');
    }
  },

  connectAliyun() {
    const { host, clientId, username, password, port, path, subscribeTopic } = aliyunConfig;

    const options = {
      clientId: 'test123|securemode=3,signmethod=hmacsha256|',
      username:  'test123&k1lyriw1yGj',
      password: 'c716ab70f1bdba5d91729dbd79135de6',
      protocol: 'wxs',
      host: 'k1lyriw1yGj.iot-as-mqtt.cn-shanghai.aliyuncs.com',
      port: '1883',
      path: '/mqtt',
      reconnectPeriod: 5000
    };

    this.client = mqtt.connect(options);

    // 连接成功回调
    this.client.on('connect', () => {
      console.log('阿里云连接成功');
      this.setData({ connectionStatus: "已连接" });
      this.client.subscribe(subscribeTopic, { qos: 1 });
    });

    // 消息处理回调
    this.client.on('message', (topic, message) => {
      try {
        const payload = JSON.parse(message);
        this.updateSensorData(payload);
      } catch (e) {
        console.error('数据解析失败:', e);
        wx.showToast({ title: '数据格式错误', icon: 'none' });
      }
    });

    // 错误处理回调
    this.client.on('error', (err) => {
      console.error('连接错误:', err);
      this.setData({ connectionStatus: "连接失败" });
      wx.showToast({ title: '物联网连接失败', icon: 'none' });
    });
  },

  updateSensorData(payload) {
    this.setData({
      'sensorData.temperature': payload.temperature?.toFixed(1) || '--',
      'sensorData.humidity': payload.humidity?.toFixed(1) || '--',
      'sensorData.airQuality': payload.aqi || '--',
      'sensorData.dust': payload.dust || '--',
      'sensorData.status': payload.status === 1
    });
  },

  // 点击事件处理
  onTapTemperature() {
    wx.showToast({
      title: `当前温度：${this.data.sensorData.temperature}℃`,
      icon: 'none',
      duration: 2000
    });
  },

  onTapHumidity() {
    wx.showModal({
      title: '湿度详情',
      content: `当前环境湿度：${this.data.sensorData.humidity}%`,
      showCancel: false
    });
  },

  onTapAirQuality() {
    const level = this.getAirQualityLevel(this.data.sensorData.airQuality);
    wx.showModal({
      title: '空气质量',
      content: `AQI指数：${this.data.sensorData.airQuality}\n等级：${level}`,
      showCancel: false
    });
  },

  onTapDust() {
    wx.showModal({
      title: '粉尘浓度',
      content: `PM2.5浓度：${this.data.sensorData.dust} μg/m³`,
      showCancel: false
    });
  },

  onTapStatus() {
    const status = this.data.sensorData.status ? '正常' : '异常';
    wx.showModal({
      title: '设备状态',
      content: `当前设备运行状态：${status}`,
      showCancel: false
    });
  },

  getAirQualityLevel(aqi) {
    if (!aqi) return '未知';
    if (aqi <= 50) return '优';
    if (aqi <= 100) return '良';
    if (aqi <= 150) return '轻度污染';
    if (aqi <= 200) return '中度污染';
    return '重度污染';
  }
});