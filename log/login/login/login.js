
const db = wx.cloud.database()
Page({
    // 登陆功能
    create_login(e) {
        let user = e.detail.value
        console.log('user', user)
        if (!user.phone) {
            wx.showToast({
                icon: 'none',
                title: '请填写手机',
            })
        } else if (!user.password) {
            wx.showToast({
                icon: 'none',
                title: '请填写密码',
            })
        } else {
            db.collection('user').where({
                    phone: user.phone,
                    password: user.password
                }).get()
                .then(res => {
                    console.log('获取登录结果', res)
                    let users = res.data
                    if (users && users.length > 0) {
                        let user = users[0]
                        wx.setStorageSync('user2', user)
                        wx.navigateTo({
                            url: '/pages/me2/me2',
                        })
                    } else {
                        wx.showToast({
                            title: '账号密码错误',
                            icon: "error"
                        })
                    }
                })
                .catch(res => {
                    console.log('获取登录结果失败', res)
                })
        }
    },
    // 去注册
    zhuce(res) {
        wx.navigateTo({
            url: '/pages/register/register',
        })
    },

})


const db = wx.cloud.database();
const dbUser = db.collection("user")
Page({
    // 注册
    reg(e) {
        let user = e.detail.value
        console.log('user', user)
        if (!user.phone) {
            wx.showToast({
                icon: 'error',
                title: '请填写手机',
            })
        } else if (!user.password) {
            wx.showToast({
                icon: 'error',
                title: '请填写密码',
            })
        } else if (!user.name) {
            wx.showToast({
                icon: 'error',
                title: '请填写姓名',
            })
        } else {
            dbUser.doc(user.phone).get()
                .then(res => {
                    console.log('查询结果', res)
                    if (res.data) {
                        wx.showToast({
                            icon: 'error',
                            title: '手机号已注册过',
                            duration: 1500
                        })
                    } else {
                        this.addUser(user)
                    }
                }).catch(res => {
                    console.log('没有注册过')
                    this.addUser(user)
                })
        }
    },
    //添加用户
    addUser(user) {
        user._id = user.phone
        // 给用户一个默认头像
        user.avatarUrl = '/image/no_login.png'
        dbUser.add({
            data: user
        }).then(res => {
            console.log('注册成功', res)
            wx.showToast({
                title: '注册成功！',
                icon: 'success',
                duration: 2500
            })
            setTimeout(function () {
                wx.navigateTo({
                    url: '/pages/login/login',
                })
            }, 1000)
        })
    }
})