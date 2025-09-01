export function getImagePath(season) {
  return `/images/${season}.jpg`
}

export function isValidSeason(season) {
  return ['Spring', 'Summer', 'Autumn', 'Winter'].includes(season)
}

export function preloadImages(paths) {
  const promises = paths.map(path => {
    return new Promise((resolve) => {
      const img = new Image()
      img.onload = () => resolve()
      img.onerror = () => resolve()
      img.src = path
    })
  })
  return Promise.all(promises)
}
