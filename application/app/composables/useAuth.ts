export type User = {
  username: string
  password: string
  id: string
  role: string
}

export type PublicUser = {
  id: string
  username: string
  role: string
}


export const useAuth = () => {
  const user = useState<PublicUser | null>('auth-user', () => null)
  const loading = useState<boolean>('auth-loading', () => true)

  const fetchUser = async () => {
    loading.value = true
    try {
      const response = await $fetch<{ user: PublicUser | null }>('/api/auth/me')
      user.value = response.user
    } catch {
      user.value = null
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    try {
      await $fetch('/api/auth/logout', { method: 'POST' })
      user.value = null
      navigateTo('/auth/login')
    } catch (e) {
      console.error(e)
    }
  }

  return {
    user,
    loading,
    fetchUser,
    logout
  }
}
