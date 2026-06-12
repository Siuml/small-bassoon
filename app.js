// app.js
const mqtt = require('./utils/mqtt.min.js');
const aliyunConfig = require('./config/aliyun');
const Crypto = require('./utils/crypto');

App({
    globalData: {
        mqttClient: null, // 全局唯一的 MQTT 客户端
        sensorData: {}
      },

  onLaunch() {
    this.initAliyunIoT();
  },

  // 初始化物联网连接
  initAliyunIoT() {
    const { clientId, deviceName, productKey, deviceSecret, host, port, path } = aliyunConfig;

    // 动态生成密码
    const content = `clientId${clientId}deviceName${deviceName}productKey${productKey}`;
    const password = Crypto.hmacsha256(content, deviceSecret).toUpperCase();

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

    this.globalData.mqttClient = mqtt.connect(options);

    // 连接成功监听
    this.globalData.mqttClient.on('connect', () => {
      console.log('[阿里云] MQTT连接成功');
      this.subscribeTopics();
    });

    // 消息处理
    this.globalData.mqttClient.on('message', (topic, payload) => {
      try {
        const data = JSON.parse(payload.toString());
        this.globalData.sensorData = data;
        // 触发全局更新
        if (this.globalData.onSensorDataUpdate) {
          this.globalData.onSensorDataUpdate(data);
        }
      } catch (e) {
        console.error('[阿里云] 消息解析失败:', e);
      }
    });

    // 错误处理
    this.globalData.mqttClient.on('error', (err) => {
      console.error('[阿里云] 连接错误:', err);
      wx.showToast({ title: '连接异常', icon: 'none' });
    });

    // 断线自动重连
    this.globalData.mqttClient.on('close', () => {
      setTimeout(() => this.initAliyunIoT(), 5000);
    });
  },

  // 订阅主题
  subscribeTopics() {
    this.globalData.mqttClient.subscribe(aliyunConfig.subscribeTopic, { qos: 1 });
  },

  globalData: {
    mqttClient: null,
    sensorData: {},
    onSensorDataUpdate: null // 数据更新回调
  }
});