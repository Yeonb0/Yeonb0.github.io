module.exports = async (tp) => {
  const title = await tp.system.prompt("Post Title (파일명 / 제목)")
  if (!title) return

  const date = tp.date.now("YYYY-MM-DD")
  const fileName = `${date}-${title}`

  await tp.file.create_new(
    tp.file.find_tfile("gitblog-cpp.md"),
    fileName
  )
}
