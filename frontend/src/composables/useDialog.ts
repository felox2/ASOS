import { getCurrentInstance, h, render, type Component } from 'vue'

export function useDialog<T>(component: Component<T>) {
  // @ts-ignore
  const { appContext } = getCurrentInstance()

  return function (props: any = {}) {
    return new Promise((resolve) => {
      function cleanup() {
        setTimeout(() => {
          render(null, root)
          root.remove()
        }, 500)
      }

      props.onClose = cleanup
      props.onSuccess = (input: any) => {
        console.log(component.name, 'success', input)

        resolve(input)
        cleanup()
      }

      const dialog = h(component, props)
      dialog.appContext = { ...appContext }

      const root = document.createElement('div')
      root.id = Math.random().toString(36).slice(2)
      document.body.appendChild(root)

      console.debug('mounting', component.name, props)

      render(dialog, root)
    })
  }
}
