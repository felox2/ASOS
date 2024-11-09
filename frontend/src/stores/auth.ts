import { client } from '@/lib/client'
import type { Middleware } from 'openapi-fetch'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

function parseToken(token: string) {
  const payloadBase64 = token.substring(
    token.indexOf('.') + 1,
    token.lastIndexOf('.')
  )
  const payload = atob(payloadBase64)

  try {
    return JSON.parse(payload) as UserTokenData
  } catch {
    return undefined
  }
}

interface UserTokenData {
  id: number
  exp: number
  username: string
  name: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<UserTokenData | undefined>()
  const token = ref<string | undefined>()
  const timerId = ref()

  const authMiddleware: Middleware = {
    onRequest({ request }) {
      console.debug('authMiddleware', token.value)

      if (!token.value) {
        return undefined
      }

      request.headers.set('Authorization', `Bearer ${token.value}`)
      return request
    },
  }

  function startRefreshTimer() {
    if (!user.value) {
      return
    }

    // 30 seconds before expiration
    const time = user.value.exp * 1000 - new Date().valueOf() - 30_000

    timerId.value = setTimeout(() => {
      console.debug('refreshing', timerId.value)
      refresh()
    }, time)

    console.debug(
      'refresh scheduled for',
      new Date(new Date().valueOf() + time).toString()
    )
  }

  async function login(input: {
    username: string
    password: string
    rememberMe: boolean
  }) {
    const { error, data } = await client.POST('/auth/login', {
      // @ts-ignore
      body: input,
      credentials: 'include',
      bodySerializer(body) {
        const data = new FormData()

        data.append('username', body.username)
        data.append('password', body.password)
        data.append('remember_me', String(input.rememberMe))

        return data
      },
    })

    if (!data?.access_token) {
      throw error
    }

    client.use(authMiddleware)

    const tokenParsed = parseToken(data.access_token)
    if (!tokenParsed) {
      console.error("couldn't parse token", data.access_token)
      return
    }

    token.value = data.access_token
    user.value = tokenParsed

    startRefreshTimer()

    return data
  }

  async function logout() {
    // @ts-ignore
    await client.POST('/auth/logout', {
      credentials: 'include',
    })

    client.eject(authMiddleware)

    token.value = undefined
    user.value = undefined

    if (timerId.value) {
      clearTimeout(timerId.value)
    }

    timerId.value = undefined
  }

  async function refresh() {
    const { data } = await client
      // @ts-ignore
      .POST('/auth/refresh', {
        credentials: 'include',
      })
      .catch(() => ({ data: undefined }))

    if (!data) {
      return
    }

    const tokenParsed = parseToken(data.access_token)
    if (!tokenParsed) {
      console.error("couldn't parse token", data.access_token)
      return
    }

    client.use(authMiddleware)

    token.value = data.access_token
    user.value = tokenParsed

    startRefreshTimer()
  }

  return {
    user,
    token,
    login,
    logout,
    refresh,
  }
})
