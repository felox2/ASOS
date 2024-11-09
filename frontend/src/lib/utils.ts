import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export async function unwrap<TData, TError>(
  responsePromise: Promise<{ data?: TData; error?: TError }>
): Promise<TData> {
  const res = await responsePromise

  if (res.error || !res.data) {
    throw res.error
  }

  return res.data
}
