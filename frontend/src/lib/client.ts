import { type paths } from '@/types/api'
import createClient from 'openapi-fetch'

export const client = createClient<paths>({
  baseUrl: import.meta.env.VITE_API_URL,
})

// error throwing middleware
client.use({
  onResponse({ response }) {
    if (response.ok) {
      return undefined
    }

    // FIXME: parse body to throw proper error
    throw new Error('test123')
  },
})
