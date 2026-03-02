export function generateStringArray() {
  const array = []
  const letters = 'abcdefghijklmnopqrstuvwxyz'
  let id = 1

  for (let i = 0; i < letters.length; i++) {
    for (let j = 0; j < letters.length; j++) {
      const str = letters[i].toUpperCase() + letters[j]
      array.push({ id: id++, label: str })
    }
  }

  return array
}
