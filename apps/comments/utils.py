from apps.comments.models import PostComment


def addMentionedUserToPostComment(postComment: PostComment, userId: int):
    try:
        postComment.mentionedUsers.add(userId)
    except ValueError:
        return postComment
    return postComment


def removeMentionedUserFromPostComment(postComment: PostComment, userId: int):
    try:
        postComment.mentionedUsers.remove(userId)
    except ValueError:
        return postComment
    return postComment
