export function initials(name: string) {
  return name
    .split(' ')
    .map((part) => part[0])
    .slice(0, 2)
    .join('')
    .toUpperCase()
}

export const dateFormatter = new Intl.DateTimeFormat('mn-MN', {
  weekday: 'long',
  day: '2-digit',
  month: 'long',
  year: 'numeric',
})

export const dateTimeFormatter = new Intl.DateTimeFormat('mn-MN', {
  day: '2-digit',
  month: 'short',
  year: 'numeric',
  hour: '2-digit',
  minute: '2-digit',
})
